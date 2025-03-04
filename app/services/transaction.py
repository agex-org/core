import json

import requests
from web3 import Web3
from web3.datastructures import AttributeDict


class TransactionService:
    def __init__(
        self, sonicscan_api_url: str, sonicscan_api_key: str, node_provider_rpc: str
    ):
        self.sonicscan_api_url = sonicscan_api_url
        self.sonicscan_api_key = sonicscan_api_key
        self.web3 = Web3(Web3.HTTPProvider(node_provider_rpc))

    # --- SonicScan API Methods ---
    def get_transaction_details_sonicscan(self, transaction_hash: str) -> str:
        try:
            params = {
                "module": "proxy",
                "action": "eth_getTransactionByHash",
                "txhash": transaction_hash,
                "apikey": self.sonicscan_api_key,
            }
            response = requests.get(self.sonicscan_api_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors.
            data = response.json()
            # If there's a "result" field, convert its numeric hex fields to integers.
            if "result" in data and isinstance(data["result"], dict):
                data["result"] = convert_numeric_hex_fields(data["result"])
            return json.dumps(data, indent=2)
        except Exception as e:
            return f"Error fetching transaction receipt from SonicScan: {e}"

    def get_transaction_receipt_sonicscan(self, transaction_hash: str) -> str:
        try:
            params = {
                "module": "transaction",
                "action": "gettxreceiptstatus",
                "txhash": transaction_hash,
                "apikey": self.sonicscan_api_key,
            }
            response = requests.get(self.sonicscan_api_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors.
            data = response.json()
            # If there's a "result" field, convert its numeric hex fields to integers.
            if "result" in data and isinstance(data["result"], dict):
                data["result"] = convert_numeric_hex_fields(data["result"])
            return json.dumps(data, indent=2)
        except Exception as e:
            return f"Error fetching transaction receipt from SonicScan: {e}"

    # --- Sonic Node (Web3) Methods ---
    def get_transaction_details_node(self, transaction_hash: str) -> str:
        try:
            tx = self.web3.eth.get_transaction(transaction_hash)
            tx_dict = dict(tx)
            # Convert any HexBytes (or similar objects with a hex() method) to a hex string.
            for key, value in tx_dict.items():
                if hasattr(value, "hex"):
                    tx_dict[key] = value.hex()
                else:
                    tx_dict[key] = value
            # Return a pretty-printed JSON string.
            return json.dumps(tx_dict, indent=2)
        except Exception as e:
            return f"Error fetching transaction receipt from SonicScan: {e}"

    def get_transaction_receipt_node(self, transaction_hash: str) -> str:
        try:
            receipt = self.web3.eth.get_transaction_receipt(transaction_hash)
            receipt_dict = dict(receipt)
            serializable_receipt = convert_to_serializable(receipt_dict)
            return json.dumps(serializable_receipt, indent=2)
        except Exception as e:
            return f"Error fetching transaction receipt from SonicScan: {e}"

    def get_transaction_logs_node(self, transaction_hash: str) -> str:
        try:
            receipt = self.web3.eth.get_transaction_receipt(transaction_hash)
            logs = receipt.logs if hasattr(receipt, "logs") else receipt.get("logs", [])
            serializable_logs = convert_to_serializable(logs)
            return json.dumps(serializable_logs, indent=2)
        except Exception as e:
            return f"Error fetching transaction receipt from SonicScan: {e}"


def convert_to_serializable(obj):
    """
    Recursively convert objects to a JSON-serializable format.
    Converts AttributeDict objects to dicts, and any object with a `hex` method to its hex string.
    """
    if isinstance(obj, AttributeDict):
        return convert_to_serializable(dict(obj))
    elif hasattr(obj, "hex"):
        return obj.hex()
    elif hasattr(obj, "items"):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    else:
        return obj


def convert_numeric_hex_fields(data):
    """
    Recursively convert specific hex string fields to integers.
    Only keys defined in numeric_keys are converted if their value is a hex string.
    """
    numeric_keys = {
        "blockNumber",
        "gas",
        "gasPrice",
        "nonce",
        "transactionIndex",
        "value",
        "gasUsed",
        "cumulativeGasUsed",
        "effectiveGasPrice",
        "logIndex",
        "maxFeePerBlobGas",
    }
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if (
                key in numeric_keys
                and isinstance(value, str)
                and value.startswith("0x")
            ):
                try:
                    new_data[key] = int(value, 16)
                except Exception:
                    new_data[key] = value
            else:
                new_data[key] = convert_numeric_hex_fields(value)
        return new_data
    elif isinstance(data, list):
        return [convert_numeric_hex_fields(item) for item in data]
    else:
        return data
