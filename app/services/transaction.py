import requests


class TransactionService:
    def __init__(self, api_url: str, api_key: str):
        self.sonicscan_api_url = api_url
        self.sonicscan_api_key = api_key

    def get_transaction_details(self, transaction_hash: str) -> str:
        params = {
            "module": "proxy",
            "action": "eth_getTransactionByHash",
            "txhash": transaction_hash,
            "apikey": self.sonicscan_api_key,
        }
        response = requests.get(self.sonicscan_api_url, params=params)
        return response.json()

    def get_transaction_receipt(self, transaction_hash: str) -> str:
        params = {
            "module": "transaction",
            "action": "gettxreceiptstatus",
            "txhash": transaction_hash,
            "apikey": self.sonicscan_api_key,
        }
        response = requests.get(self.sonicscan_api_url, params=params)
        return response.json()
