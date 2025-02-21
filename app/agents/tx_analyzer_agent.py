# app/agents/tx_analyzer_agent.py

from app.agents.base import BaseAgent


class TxAnalyzerAgent(BaseAgent):
    def handle_query(self, query: str, chat_history: list = None) -> str:
        # Here you might use web3.py to fetch transaction data and analyze it.
        return (
            "Transaction Analysis: The provided transaction has normal gas usage and the address "
            "behaves as expected. No suspicious patterns detected."
        )
