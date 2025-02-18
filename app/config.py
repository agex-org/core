import os


class Config:
    # OpenAI configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    MAX_TOKENS = 10

    # Agent names
    BLOCKCHAIN_EDUCATOR_NAME = "Blockchain Educator"
    CONTRACT_AUDITOR_NAME = "Contract Auditor"
    TX_ADDRESS_ANALYZER_NAME = "Transaction/Address Analyzer"

    # Redis configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
