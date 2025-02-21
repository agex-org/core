from typing import Type

from app.agents.analyzer_agent import TxAddressAnalyzerAgent
from app.agents.auditor.agent import ContractAuditorAgent
from app.agents.base import BaseAgent
from app.agents.educator.agent import BlockchainEducatorAgent
from app.config import Config

agents: dict[str, Type[BaseAgent]] = {
    Config.BLOCKCHAIN_EDUCATOR_NAME.lower(): BlockchainEducatorAgent,
    Config.CONTRACT_AUDITOR_NAME.lower(): ContractAuditorAgent,
    Config.TX_ADDRESS_ANALYZER_NAME.lower(): TxAddressAnalyzerAgent,
}
