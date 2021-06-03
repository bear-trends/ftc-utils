from .importer import Importer
from .exporter import Exporter
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
import boto3
import os
import json


def load_importer_exporter(
    mode='local',
    aws_bucket='',
    local_path=''
):
    """Make importer and exporter classes

    Args:
        mode (str, optional): exporting mode, s3 or local.
            Defaults to 'local'.
        aws_bucket (str, optional): if mode = 's3'.
            Defaults to ''.
        local_path (str, optional): if mode = 'local'.
            Defaults to ''.

    Returns:
        [utils.Importer]: Importer module
        [utils.Exporter]: Exporter module
    """
    importer = Importer(
        mode=mode,
        aws_bucket=aws_bucket,
        local_path=local_path
    )

    exporter = Exporter(
        mode=mode,
        aws_bucket=aws_bucket,
        local_path=local_path
    )

    return importer, exporter


def get_es_connection():
    """Get elastic search connection object

    Returns:
        [elasticsearch.Elasticsearch]: connection object
    """

    s3_client = boto3.client(
        service_name='s3'
    )

    key_file = s3_client.get_object(
        Bucket='ftc-data-storage', Key='api_keys.json'
    )['Body'].read()

    host = key_file['es_instance_host']
    region = 'eu-west-3'
    service = 'es'
    credentials = boto3.Session().get_credentials()

    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region, service,
        session_token=credentials.token
    )

    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    return es


def make_es_indices(
    tables=[
        'items',
        'users',
        'brands',
        'photos',
        'accounts'
    ]
):
    """Creates indexes on aws s3
    according to mappings

    Args:
        tables (list, optional): indexes to create
            Defaults to [ 'items', 'users', 'brands', 'photos', 'accounts' ].
    """
    es = get_es_connection()
    folder_path = os.path.dirname(os.path.abspath(__file__))
    for table in tables:
        table_path = f'/mappings/{table}.json'
        path = os.path.join(folder_path, table_path)
        with open(path, 'r') as f:
            mapping = json.load(f)
        es.indices.create(
            index=table,
            body=mapping
        )
