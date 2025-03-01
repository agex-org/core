from app.services.chat_history_service import ChatHistoryService
from app.services.classification_service import ClassificationService
from app.services.title_service import TitleGenerator

classifier = ClassificationService()
chat_history = ChatHistoryService()
title_generator = TitleGenerator()
