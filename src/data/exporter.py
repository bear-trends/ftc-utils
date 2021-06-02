from io import BytesIO
import datetime
import pickle
import boto3
import uuid
import os


class Exporter:
    """Class to export sourcing results
    to s3 or locally
    """

    def __init__(
        self,
        mode='local',
        aws_bucket='',
        local_path=''
    ):
        """Init class

        Args:
            mode (str, optional): exporting mode, s3 or local.
                Defaults to 'local'.
            aws_bucket (str, optional): if mode = 's3'.
                Defaults to ''.
            local_path (str, optional): if mode = 'local'.
                Defaults to ''.
        """
        # Break if invalid mode
        assert mode in ['s3', 'local']

        self.mode = mode
        self.today = datetime.datetime.today().strftime('%d_%m_%Y')

        if mode == 's3':
            self.aws_bucket = aws_bucket

            # Create bot3 client
            self.s3_client = boto3.client(
                service_name='s3'
            )

        elif mode == 'local':
            self.local_path = local_path

    def dataframe_to_s3(self, df, filepath):

        # Write dataframe to buffer
        out_buffer = BytesIO()

        # Fastparquet doesn't support saving like this
        # so we use pyarrow
        df.to_parquet(
            out_buffer,
            index=False,
            engine='pyarrow',
            compression='gzip'
        )

        # Export buffer content to s3
        self.s3_client.put_object(
            Bucket=self.aws_bucket,
            Key=filepath,
            Body=out_buffer.getvalue()
        )

    def _export_results_s3(
        self,
        sourced_pages,
        results
    ):
        """Export results to s3

        Args:
            sourced_pages (list): see export_results
            results (dict): see export_results
        """

        # Saved sourced paged list
        sourced_pages_pickle = pickle.dumps(sourced_pages)
        sourced_pages_path = f'{self.today}/sourced_pages.pickle'
        self.s3_client.put_object(
            Body=sourced_pages_pickle,
            Bucket=self.aws_bucket,
            Key=sourced_pages_path
        )

        # Save results per category
        for category in results.keys():
            category_results_path = (
                f'{self.today}/{category}/'
                f'{uuid.uuid4().hex}_sourcing_results.parquet.gzip'
            )
            self.dataframe_to_s3(
                results[category],
                category_results_path
            )

    def _export_results_local(
        self,
        sourced_pages,
        results
    ):
        """Export results to local

        Args:
            sourced_pages (list): see export_results
            results (dict): see export_results
        """
        # Make folder for saving today's results if doesn't exist
        today_folder_path = os.path.join(
            self.local_path, f'{self.today}'
        )
        if not os.path.exists(today_folder_path):
            os.makedirs(today_folder_path)

        # Save sourced pages list
        sourced_pages_path = os.path.join(
            today_folder_path,
            'sourced_pages.pickle'
        )

        with open(sourced_pages_path, 'wb') as f:
            pickle.dump(sourced_pages, f)

        # Save results per category
        for category in results.keys():

            # Create category folder if doesn't exist
            category_folder_path = os.path.join(
                self.local_path,
                f'{self.today}/{category}'
            )
            if not os.path.exists(category_folder_path):
                os.makedirs(category_folder_path)

            # Save results as parquet
            category_results_path = os.path.join(
                category_folder_path,
                f'{uuid.uuid4().hex}_sourcing_results.parquet.gzip'
            )

            results[category].to_parquet(
                category_results_path,
                engine='pyarrow',
                compression='gzip'
            )

    def export_results(
        self,
        sourced_pages,
        results
    ):
        """Export sourcing results to s3 or local depending
        on mode

        Args:
            sourced_pages (list): list of pages sourced
            results (dictionnary): dict of the form {category: pd.DataFrame}
        """
        if self.mode == 's3':
            self._export_results_s3(
                sourced_pages,
                results
            )
        elif self.mode == 'local':
            self._export_results_local(
                sourced_pages,
                results
            )
