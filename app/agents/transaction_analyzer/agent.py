# app/agents/agent.py
from web3 import Web3

from app.agents.base import BaseAgent
from app.config import Config


class TransactionAnalyzerAgent(BaseAgent):
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(Config.Sonic_NODE_URL))

    def handle_query(self, query: str, chat_history: list = None) -> str:
        """
        Analyzes a transaction on the Sonic Network given its transaction hash.

        Expects the query to be a valid transaction hash (66 characters long, starting with '0x').
        Fetches transaction details and receipt from the Sonic Network and compiles a basic analysis report.
        """
        tx_hash = query.strip()

        # Basic validation of the transaction hash format.
        if not (tx_hash.startswith("0x") and len(tx_hash) == 66):
            return "Invalid transaction hash provided. Please provide a valid transaction hash for the Sonic Network."

        try:
            tx = self.web3.eth.get_transaction(tx_hash)
            tx_receipt = self.web3.eth.get_transaction_receipt(tx_hash)
        except Exception as e:
            return f"Error fetching transaction details from Sonic Network: {e}"
