import os

import httpx
from dotenv import load_dotenv


load_dotenv()


BASE_URL = os.getenv("BASE_URL", "https://secby.ru")


class ApiClient:
    def __init__(self, token=None):
        self.client = httpx.Client(base_url=BASE_URL)

        if token:
            self.client.headers.update({
                "Authorization": f"Bearer {token}"
            })

    def post(self, url, json=None):
        return self.client.post(url, json=json)

    def get(self, url):
        return self.client.get(url)