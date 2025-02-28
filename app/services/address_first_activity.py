import requests


class AddressFirstActivityService:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def get_first_activity(self, address: str) -> str:
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "apikey": self.api_key,
            "startblock": 0,
            "endblock": 99999999,
            "page": 1,
            "offset": 1,
            "sort": "asc",
        }
        response = requests.get(self.api_url, params=params)
        return response.json()
