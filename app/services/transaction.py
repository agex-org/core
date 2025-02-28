import requests
from web3 import Web3


class TransactionService:
    def __init__(
        self, sonicscan_api_url: str, sonicscan_api_key: str, node_provider_rpc: str
    ):
        self.sonicscan_api_url = sonicscan_api_url
        self.sonicscan_api_key = sonicscan_api_key
        self.web3 = Web3(Web3.HTTPProvider(node_provider_rpc))

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
