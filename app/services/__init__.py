from app.agents.orchestrator.agent import OrchestratorAgent
from app.services.chat_history_service import ChatHistoryService
from app.services.title_service import TitleGenerator

orchestrator = OrchestratorAgent()
chat_history = ChatHistoryService()
title_generator = TitleGenerator()
