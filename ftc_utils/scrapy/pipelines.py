import datetime
import gc
import pickle
import pandas as pd
from elasticsearch import helpers
from ..data.exporter import Exporter
from ..data.api import get_es_connection


class S3Pipeline(object):
    def __init__(self, bucket_name):
        """Initialize.
        Args:
            bucket_name (str): Name of the bucket to store items in.
            platform (str): Name of the platform that is used as an s3 key
                prefix, i.e. 'thuisbezorgd' or 'ubereats'.
        """
        # Injected by self.open_spider
        self.exporter = Exporter(mode="s3", aws_bucket=bucket_name)
        self.results = {}
        self.max_items_buffer = 50000
        self.current_hold_items = 0

    def save_results(self, spider):
        print(f'Reached buffer size of {self.max_items_buffer}')
        print("Exporting results to s3...")
        self.results = {
            x: pd.DataFrame(y).applymap(str) for x, y in self.results.items()
        }
        self.exporter.export_results(spider.sourced_pages, self.results)

    def close_spider(self, spider):
        self.save_results(spider)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            bucket_name=crawler.settings.get("BUCKET_NAME"),
        )

    def process_item(self, item, spider):
        self.current_hold_items += 1
        if self.current_hold_items > self.max_items_buffer:
            self.save_results(spider)
            self.current_hold_items = 0
            del self.results
            self.results = {}
            gc.collect()
            print('Cleaned results from memory')

        if spider.current_category not in self.results.keys():
            self.results[spider.current_category] = []
        self.results[spider.current_category].append(item)
        return item


class ElasticsearchPipeline(object):
    """Pipeline saving locacally on ElasticSearch
    """

    def __init__(
        self,
        platform,
        bucket_name,
        max_items_buffer,
        saved_indexes
    ):
        self.bucket_name = bucket_name
        self.platform = platform
        self.es = get_es_connection()
        self.exporter = Exporter(mode="s3", aws_bucket=bucket_name)
        self.results = {}
        self.current_hold_items = 0
        self.max_items_buffer = max_items_buffer
        self.saved_indexes = saved_indexes

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            platform=crawler.settings.get("PLATFORM"),
            bucket_name=crawler.settings.get("BUCKET_NAME"),
            max_items_buffer=crawler.settings.get("MAX_ITEMS_BUFFER"),
            saved_indexes=crawler.settings.get("SAVED_INDEXES")
        )

    def get_upload_generator(self):
        for index, rows in self.results.items():
            # pass if index not in saved_indexes
            if self.saved_indexes and index not in self.saved_indexes:
                continue
            for row in rows:
                # id is platform + id to avoid duplicates
                # inbetween platforms
                yield {
                    "_index": index,
                    "_id": f"{self.platform}_{row['id']}",
                    "_source": row
                }

    def save_results(self):
        generator = self.get_upload_generator()
        helpers.bulk(self.es, generator)
        self.results = {}
        self.current_hold_items = 0

    def close_spider(self, spider):
        sourced_pages_pickle = pickle.dumps(spider.sourced_pages)
        sourced_pages_path = f'{self.exporter.today}/sourced_pages.pickle'
        self.exporter.s3_client.put_object(
            Body=sourced_pages_pickle,
            Bucket=self.bucket_name,
            Key=sourced_pages_path
        )
        self.save_results()

    def process_item(self, item, spider):
        index = item.es_index
        item['platform'] = self.platform
        item['sourced_at'] = datetime.datetime.now().strftime(
            '%d/%m/%Y %H:%M'
        )
        if index in self.results.keys():
            self.results[index].append(dict(item))
        else:
            self.results[index] = [dict(item)]
        self.current_hold_items += 1
        if self.current_hold_items > self.max_items_buffer:
            print('Reached max buffer size')
            print('Saving results')
            self.save_results()
        return item
