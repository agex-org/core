# app/agents/address_analyzer_agent.py

from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

from app.agents.base import BaseAgent
from app.config import Config
from app.services.batch_balance.base import BatchBalanceService


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

        tools = [self.balance_tool]

        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

        self.agent.handle_parsing_errors = True
