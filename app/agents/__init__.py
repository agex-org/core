from app.agents.analyzer_agent import TxAddressAnalyzerAgent
from app.agents.auditor_agent import ContractAuditorAgent
from app.agents.educator.agent import BlockchainEducatorAgent
from app.config import Config

agents = {
    Config.BLOCKCHAIN_EDUCATOR_NAME.lower(): BlockchainEducatorAgent(),
    Config.CONTRACT_AUDITOR_NAME.lower(): ContractAuditorAgent(),
    Config.TX_ADDRESS_ANALYZER_NAME.lower(): TxAddressAnalyzerAgent(),
}
