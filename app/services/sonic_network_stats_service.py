import requests


class SonicNetworkStatsService:
    def __init__(self, sonicscan_api_url: str, sonicscan_api_key: str):
        self.sonicscan_api_url = sonicscan_api_url
        self.sonicscan_api_key = sonicscan_api_key

    def get_block_height(self) -> int:
        """
        Fetches the current block height (latest block number) from Ethereum.
        """
        params = {
            "module": "proxy",
            "action": "eth_blockNumber",
            "apikey": self.sonicscan_api_key,
        }
        response = requests.get(self.sonicscan_api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors.
        data = response.json()
        if "result" in data:
            # The result is returned as a hex string; convert it to int.
            return int(data["result"], 16)
        else:
            raise Exception(
                "Failed to get block height: " + data.get("message", "Unknown error")
            )

    def get_transaction_count_last_24h(self) -> int:
        """
        Returns the total number of transactions in the last 24 hours.
        NOTE: This endpoint is a placeholder. Replace 'txcount24h' with a valid action
        from your data provider or aggregator.
        """
        params = {
            "module": "stats",
            "action": "txcount24h",  # Placeholder endpoint – replace with a valid one.
            "apikey": self.sonicscan_api_key,
        }
        response = requests.get(self.sonicscan_api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors.
        data = response.json()
        if "result" in data:
            return int(data["result"])
        else:
            raise Exception(
                "Failed to get tx count in last 24h: "
                + data.get("message", "Unknown error")
            )

    def get_active_addresses_last_24h(self) -> int:
        """
        Returns the number of unique active addresses in the last 24 hours.
        NOTE: This endpoint is a placeholder. Replace 'activeaddresses24h' with a valid action
        from your data provider or aggregator.
        """
        params = {
            "module": "stats",
            "action": "activeaddresses24h",  # Placeholder endpoint – replace with a valid one.
            "apikey": self.sonicscan_api_key,
        }
        response = requests.get(self.sonicscan_api_url, params=params)
        data = response.json()
        if "result" in data:
            return int(data["result"])
        else:
            raise Exception(
                "Failed to get active addresses in last 24h: "
                + data.get("message", "Unknown error")
            )
