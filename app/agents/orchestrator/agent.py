from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

from app.agents.address_analyzer.agent import AddressAnalyzerAgent
from app.agents.auditor.agent import ContractAuditorAgent
from app.agents.base import BaseAgent
from app.agents.educator.agent import BlockchainEducatorAgent
from app.agents.transaction_analyzer.agent import TransactionAnalyzerAgent
from app.config import Config


class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__()

        # Initialize LLM
        self.llm = ChatOpenAI(
            openai_api_key=Config.OPENAI_API_KEY,
            openai_api_base=Config.OPENAI_BASE_URL,
            model=Config.OPENAI_MODEL,
            temperature=0,
        )

        # Initialize all specialized agents
        self.address_analyzer = AddressAnalyzerAgent()
        self.contract_auditor = ContractAuditorAgent()
        self.blockchain_educator = BlockchainEducatorAgent()
        self.transaction_analyzer = TransactionAnalyzerAgent()

        # Create tools for each specialized agent
        self.address_analyzer_tool = Tool(
            name="Address Analyzer",
            func=self.address_analyzer.handle_query,
            description="Analyzes blockchain addresses, providing information about balances, contract status, and activity history",
        )

        self.contract_auditor_tool = Tool(
            name="Contract Auditor",
            func=self.contract_auditor.handle_query,
            description="Audits smart contracts for vulnerabilities and security issues",
        )

        self.blockchain_educator_tool = Tool(
            name="Blockchain Educator",
            func=self.blockchain_educator.handle_query,
            description="Provides educational information about blockchain concepts, technologies, and terminology",
        )

        self.transaction_analyzer_tool = Tool(
            name="Transaction Analyzer",
            func=self.transaction_analyzer.handle_query,
            description="Analyzes blockchain transactions, providing detailed information about transaction data and effects",
        )

        # Initialize the orchestrator agent with all tools
        tools = [
            self.address_analyzer_tool,
            self.contract_auditor_tool,
            self.blockchain_educator_tool,
            self.transaction_analyzer_tool,
        ]

        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

        self.agent.handle_parsing_errors = True
