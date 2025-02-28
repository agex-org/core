from web3 import Web3


class IsContractService:
    def __init__(self, rpc_url: str):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

    def is_contract(self, address: str) -> bool:
        return self.w3.eth.get_code(address) != b""
