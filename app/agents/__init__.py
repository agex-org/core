from typing import Type

from app.agents.address_analyzer.agent import AddressAnalyzerAgent
from app.agents.auditor.agent import ContractAuditorAgent
from app.agents.base import BaseAgent
from app.agents.educator.agent import BlockchainEducatorAgent
from app.agents.transaction_analyzer.agent import TransactionAnalyzerAgent
from app.config import Config

agents: dict[str, Type[BaseAgent]] = {
    Config.BLOCKCHAIN_EDUCATOR_NAME.lower(): BlockchainEducatorAgent,
    Config.CONTRACT_AUDITOR_NAME.lower(): ContractAuditorAgent,
    Config.ADDRESS_ANALYZER_NAME.lower(): AddressAnalyzerAgent,
    Config.TX_ANALYZER_NAME.lower(): TransactionAnalyzerAgent,
}
