from typing import Type

from app.agents.address_analyzer.agent import AddressAnalyzerAgent
from app.agents.auditor.agent import ContractAuditorAgent
from app.agents.base import BaseAgent
from app.agents.educator.agent import BlockchainEducatorAgent
from app.agents.tx_analyzer_agent import TxAnalyzerAgent
from app.config import Config

agents: dict[str, Type[BaseAgent]] = {
    Config.BLOCKCHAIN_EDUCATOR_NAME.lower(): {
        "agent": BlockchainEducatorAgent,
        "description": "Use this tool when you need to explain blockchain concepts or provide educational information",
    },
    Config.CONTRACT_AUDITOR_NAME.lower(): {
        "agent": ContractAuditorAgent,
        "description": "Use this tool when you need to analyze smart contracts for security vulnerabilities",
    },
    Config.ADDRESS_ANALYZER_NAME.lower(): {
        "agent": AddressAnalyzerAgent,
        "description": "Use this tool when you need to analyze blockchain addresses, their balances, and activities",
    },
    Config.TX_ANALYZER_NAME.lower(): {
        "agent": TxAnalyzerAgent,
        "description": "Use this tool when you need to analyze blockchain transactions",
    },
}
