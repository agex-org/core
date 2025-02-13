import os


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    MAX_TOKENS = 10
    BLOCKCHAIN_EDUCATOR_NAME = "Blockchain Educator"
    CONTRACT_AUDITOR_NAME = "Contract Auditor"
    TX_ADDRESS_ANALYZER_NAME = "Transaction/Address Analyzer"
