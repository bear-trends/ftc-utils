import os
import json
import boto3
import pickle
import requests
import datetime
import pandas as pd
from io import BytesIO
from botocore.exceptions import ClientError


class Importer:
    """Class to manage imports of sourcing results
    """

    def __init__(
        self,
        mode='local',
        aws_bucket='',
        local_path='',
        date='today'
    ):
        """Init class

        Args:
            mode (str, optional): importing mode, s3 or local.
                Defaults to 'local'.
            aws_bucket (str, optional): if mode = 's3'.
                Defaults to ''.
            local_path (str, optional): if mode = 'local'.
                Defaults to ''.
            date (datetime, optional): date to load from, format %d_%m_%Y
                Defaults to 'today'

        """
        # Break if invalid mode
        assert mode in ['s3', 'local']

        self.mode = mode
        if date == 'today':
            self.date = datetime.datetime.today().strftime('%d_%m_%Y')
        else:
            self.date = date

        if mode == 's3':
            self.aws_bucket = aws_bucket

            # Create bot3 client
            # Credentials shoud be saved in ~/.aws/credentials
            self.s3_client = boto3.client(
                service_name='s3'
            )

        elif mode == 'local':
            self.local_path = local_path

    def _load_category_results_s3(self, category):
        """Loads category results if mode is 's3'

        Args:
            category (str): see load_category_results

        Returns:
            [pd.DataFrame]: concatenated sourcing results for category
            at self.date
        """
        path = f"{self.date}/{category}/"

        # List s3 keys of sourcing results
        try:
            file_paths = []

            for file in self.s3_client.list_objects(
                Bucket=self.aws_bucket,
                Prefix=path,
                Delimiter="/"
            )["Contents"]:
                file_paths.append(file["Key"])

        except Exception:
            file_paths = []

        # If no file is found, return empty dataframe
        if len(file_paths) == 0:
            return pd.DataFrame()

        # Load file contents using boto3 and pyarrow
        file_contents = []
        for filepath in file_paths:
            file_obj = self.s3_client.get_object(
                Bucket=self.aws_bucket,
                Key=filepath
            )
            df = pd.read_parquet(
                BytesIO(
                    file_obj["Body"].read()
                ),
                engine='pyarrow'
            )
            file_contents.append(
                df
            )

        # Return Concatenated results
        return pd.concat(
            file_contents
        )

    def _load_category_results_local(self, category):
        """Loads category results if mode is 'local'

        Args:
            category (str): see load_category_results

        Returns:
            [pd.DataFrame]: concatenated sourcing results for category
            at self.date
        """

        # Make results folder path
        path = os.path.join(
            self.local_path, f"{self.date}/{category}"
        )

        # If no files, return empty dataframe
        if not os.path.exists(path):
            return pd.DataFrame()

        # List files under path
        result_paths = os.listdir(path)

        # Otherwise, read and return dataframes
        results = pd.concat(
            [
                pd.read_parquet(
                    os.path.join(path, x), engine='pyarrow'
                ) for x in result_paths
            ]
        )
        return results

    def load_category_results(self, category):
        """Loads category results, from local folder or s3,
        for self.date and given category

        Args:
            category (str): category of results to load
            like 'chaussures'

        Returns:
            [pd.DataFrame]: concatenated results
        """

        if self.mode == 's3':
            return self._load_category_results_s3(category)

        elif self.mode == 'local':
            return self._load_category_results_local(category)

    def load_sourced_pages(self):
        """Loads list of sourced pages
        at self.date

        Returns:
            [list]: list of sourced urls
        """

        if self.mode == 'local':

            # Make path to sourced pages at self.date
            today_folder_path = os.path.join(
                self.local_path, f'{self.date}'
            )
            sourced_pages_path = os.path.join(
                today_folder_path,
                'sourced_pages.pickle'
            )

            # If path does not exists, return empty list
            if not os.path.exists(sourced_pages_path):
                return []

            with open(sourced_pages_path, 'rb') as f:
                return pickle.load(f)

        elif self.mode == "s3":

            # Make path to sourced pages at self.date
            sourced_pages_path = f'{self.date}/sourced_pages.pickle'

            try:
                # Load and return object
                obj = self.s3_client.get_object(
                    Bucket=self.aws_bucket,
                    Key=sourced_pages_path
                )
                return pickle.loads(obj["Body"].read())
            except ClientError as e:

                # If object does not exists, return empty list
                if e.response['Error']['Code'] == 'NoSuchKey':
                    return []
                else:
                    raise e

    def get_proxies(self):
        """Load api key from s3, query proxy6 api and return
        proxy list

        Returns:
            [list]: list of proxies as dictionnaries
        """

        key_file = self.s3_client.get_object(
            Bucket='ftc-data-storage', Key='api_keys.json'
        )['Body'].read()
        api_key = json.loads(key_file)['proxy6']
        proxies = requests.get(
            f'https://proxy6.net/api/{api_key}/getproxy'
        )
        proxies = list(json.loads(proxies.text)['list'].values())
        return proxies
