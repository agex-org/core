from web3 import Web3


class IsContractService:
    def __init__(self, rpc_url: str):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))

    def is_contract(self, address: str) -> bool:
        # return self.w3.eth.get_code(address) != b""
        try:
            # Convert to checksum address
            checksum_address = self.web3.to_checksum_address(address)
        except Exception as e:
            raise ValueError(f"Invalid address provided: {e}")
            # Get the contract code at the address
        code = self.web3.eth.get_code(checksum_address)
        # If code exists (non-empty), it's a contract
        return code != b""  # or len(code) > 0
