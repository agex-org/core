import requests


class TransactionService:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def get_transaction_details(self, transaction_hash: str) -> str:
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

    def get_transaction_receipt(self, transaction_hash: str) -> str:
        params = {
            "module": "transaction",
            "action": "gettxreceiptstatus",
            "txhash": transaction_hash,
            "apikey": self.api_key,
        }
        response = requests.get(self.api_url, params=params)
        return response.json()
