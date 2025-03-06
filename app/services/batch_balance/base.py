from pydantic import BaseModel
from web3 import Web3

from app.services.batch_balance.abi import abi
from app.services.batch_balance.tokens import tokens


class Balance(BaseModel):
    address: str
    token: str
    balance: float


class BatchBalanceService:
    def __init__(self, rpc: str, address: str):
        self.web3 = Web3(Web3.HTTPProvider(rpc))
        self.contract = self.web3.eth.contract(address=address, abi=abi)

    def get_batch_balance(self, address: str) -> list[Balance]:
        address = address.strip()
        try:
            checksum_address = self.web3.to_checksum_address(address)
        except Exception as e:
            raise ValueError(f"Invalid address provided: {e}")
        token_addresses = list(tokens.keys())
        balances = self.contract.functions.getAllTokensBalances(
            [checksum_address], token_addresses
        ).call()
        balances_list = []
        for balance in balances:
            balance_obj = Balance(
                address=checksum_address,
                token=tokens[balance[1]]["symbol"],
                balance=round(balance[2] / 10 ** tokens[balance[1]]["decimals"], 3),
            )
            balances_list.append(balance_obj)

        # Use checksum_address here too
        sonic_balance = self.web3.eth.get_balance(checksum_address)
        sonic_balance_obj = Balance(
            address=checksum_address,
            token="SONIC",
            balance=round(sonic_balance / 10**18, 3),
        )
        balances_list.append(sonic_balance_obj)
        return balances_list
