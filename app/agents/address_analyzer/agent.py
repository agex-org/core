# app/agents/address_analyzer_agent.py

from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

from app.agents.base import BaseAgent
from app.config import Config
from app.services.address_first_activity import AddressFirstActivityService
from app.services.batch_balance.base import BatchBalanceService
from app.services.is_contract_service import IsContractService
from app.services.timestamp_to_data import TimestampToDataService


class AddressAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.llm = ChatOpenAI(
            openai_api_key=Config.OPENAI_API_KEY,
            openai_api_base=Config.OPENAI_BASE_URL,
            model=Config.OPENAI_MODEL,
        )

        self.batch_balance_service = BatchBalanceService(
            Config.SONIC_RPC_URL, Config.BATCH_BALANCE_CONTRACT_ADDRESS
        )

        self.balance_tool = Tool(
            name="Get Balances of Address",
            func=self.batch_balance_service.get_batch_balance,
            description="Get the token balances of a given address",
        )

        self.is_contract_service = IsContractService(Config.SONIC_RPC_URL)
        self.is_contract_tool = Tool(
            name="Is Contract",
            func=self.is_contract_service.is_contract,
            description="Check if a given address is a contract",
        )
        self.address_first_activity_service = AddressFirstActivityService(
            Config.SONICSCAN_API_URL, Config.SONICSCAN_API_KEY
        )
        self.first_activity_tool = Tool(
            name="Get First Activity of Address",
            func=self.address_first_activity_service.get_first_activity,
            description="Get the first activity of a given address",
        )

        self.timestamp_to_data_service = TimestampToDataService()
        self.timestamp_to_data_tool = Tool(
            name="Timestamp to Data",
            func=self.timestamp_to_data_service.get_data,
            description="Convert a timestamp to a date and time",
        )
        tools = [
            self.balance_tool,
            self.first_activity_tool,
            self.is_contract_tool,
            self.timestamp_to_data_tool,
        ]

        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

        self.agent.handle_parsing_errors = True
