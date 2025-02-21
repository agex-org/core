import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # OpenAI configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    MAX_TOKENS = 10

    # Feed configuration
    FEED_AUDITOR = os.getenv("FEED_AUDITOR", "False") == "True"
    FEED_EDUCATOR = os.getenv("FEED_EDUCATOR", "False") == "True"

    # Agent names
    BLOCKCHAIN_EDUCATOR_NAME = "Blockchain Educator"
    CONTRACT_AUDITOR_NAME = "Contract Auditor"
    TX_ADDRESS_ANALYZER_NAME = "Transaction/Address Analyzer"

    # Redis configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    # Etherscan API configuration
    SONICSCAN_API_URL = "https://api.sonicscan.org/api"
    SONICSCAN_API_KEY = os.getenv("SONICSCAN_API_KEY")
