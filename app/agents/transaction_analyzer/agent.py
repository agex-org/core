# app/agents/agent.py
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

from app.agents.base import BaseAgent
from app.config import Config
from app.services.is_contract_service import IsContractService
from app.services.timestamp_to_data import TimestampToDataService
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

        # Tools for fetching data from SonicScan.
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

        # Tools for fetching data directly from the Sonic Node.
        self.node_tx_detail_tool = Tool(
            name="Get Transaction Details From Sonic Node",
            func=self.transaction_service.get_transaction_details_node,
            description="Fetches detailed transaction information directly from the Sonic Node",
        )

        self.node_tx_receipt_tool = Tool(
            name="Get Transaction Receipt From Sonic Node",
            func=self.transaction_service.get_transaction_receipt_node,
            description="Retrieves the transaction receipt directly from the Sonic Node",
        )

        self.node_tx_receipt_tool = Tool(
            name="Get Transaction Logs From Sonic Node",
            func=self.transaction_service.get_transaction_logs_node,
            description="Retrieves the transaction logs directly from the Sonic Node",
        )

        # Timestamp to Data
        self.timestamp_to_data_service = TimestampToDataService()
        self.timestamp_to_data_tool = Tool(
            name="Timestamp to Data",
            func=self.timestamp_to_data_service.get_data,
            description="Convert a timestamp to a date and time",
        )

        # Is Contract
        self.is_contract_service = IsContractService(Config.SONIC_NODE_RPC_URL)
        self.is_contract_tool = Tool(
            name="Is Contract",
            func=self.is_contract_service.is_contract,
            description="Check if a given address is a contract",
        )

        tools = [
            self.tx_detail_tool,
            self.tx_receipt_tool,
            self.node_tx_detail_tool,
            self.node_tx_receipt_tool,
        ]

        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

        self.agent.handle_parsing_errors = True
