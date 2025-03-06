from app.config import Config
from app.services.chat_history_service import ChatHistoryService
from app.services.classification_service import ClassificationService
from app.services.sonic_network_stats_service import SonicNetworkStatsService
from app.services.title_service import TitleGenerator

classifier = ClassificationService()
chat_history = ChatHistoryService()
title_generator = TitleGenerator()
stats_service = SonicNetworkStatsService(
    sonicscan_api_url=Config.SONICSCAN_API_URL,
    sonicscan_api_key=Config.SONICSCAN_API_KEY,
)
