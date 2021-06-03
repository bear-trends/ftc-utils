import random
from ..data.importer import Importer


class CustomProxyMiddleware(object):

    def __init__(self):
        self.importer = Importer(
            mode='s3',
            aws_bucket='ftc-data-storage',
        )
        proxy_list = self.importer.get_proxies()
        self.proxy_strings = [
            f"http://{x['user']}:{x['pass']}@{x['host']}:{x['port']}"
            for x in proxy_list
        ]

    def process_request(self, request, spider):
        request.meta["proxy"] = random.choice(
            self.proxy_strings
        )
