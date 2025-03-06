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

    def get_total_supply_of_ether(self) -> int:
        params = {
            "module": "stats",
            "action": "ethsupply",
            "apikey": self.sonicscan_api_key,
        }
        response = requests.get(self.sonicscan_api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors.
        data = response.json()
        if "result" in data:
            return int(data["result"]) // int(1e18)
        else:
            raise Exception(
                "Failed to get total supply of ether: "
                + data.get("message", "Unknown error")
            )

    def get_ether_last_price(self) -> dict():
        params = {
            "module": "stats",
            "action": "ethprice",
            "apikey": self.sonicscan_api_key,
        }
        response = requests.get(self.sonicscan_api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors.
        data = response.json()
        if "result" in data:
            return data["result"]
        else:
            raise Exception(
                "Failed to get total supply of ether: "
                + data.get("message", "Unknown error")
            )
