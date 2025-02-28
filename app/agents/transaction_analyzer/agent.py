# app/agents/agent.py
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

from app.agents.base import BaseAgent
from app.config import Config
from app.services.transaction import TransactionService


class TransactionAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__()

        # Initialize the LLM for transaction analysis
        self.llm = ChatOpenAI(
            openai_api_key=Config.OPENAI_API_KEY,
            openai_api_base=Config.OPENAI_BASE_URL,
            model=Config.OPENAI_MODEL,
        )

        # Transaction Service
        self.transaction_service = TransactionService(
            Config.SONICSCAN_API_URL,
            Config.SONICSCAN_API_KEY,
            Config.SONIC_NODE_RPC_URL,
        )

        self.tx_detail_tool = Tool(
            name="Get Transaction Details From SonicScan",
            func=self.transaction_service.get_transaction_details_sonicscan,
            description="Fetches detailed information for a given transaction hash from the Sonic Blockchain Explorer",
        )

        self.tx_receipt_tool = Tool(
            name="Get Transaction Receipt From SonicScan",
            func=self.transaction_service.get_transaction_receipt_sonicscan,
            description="Retrieves the receipt for a given transaction hash from the Sonic Blockchain Explorer",
        )

        # # Service to structure the final analysis of the transaction.
        # self.tx_analysis_formatter = TxAnalysisFormatter(self.llm)
        # self.tx_analysis_tool = Tool(
        #     name="Structure Transaction Analysis",
        #     func=self.tx_analysis_formatter.format_analysis,
        #     description="Structures a final summary of the transaction analysis, including status, gas usage, and key details",
        # )

        tools = [
            self.tx_detail_tool,
            self.tx_receipt_tool,
            # self.tx_analysis_tool,
        ]

        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

        self.agent.handle_parsing_errors = True

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
