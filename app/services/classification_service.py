# app/services/classification_service.py

from typing import Dict, List

from app.agents.educator.agent import OllamaLLM
from app.config import Config


class ClassificationService:
    def __init__(self):
        self.llm = OllamaLLM(model_name="llama2:7b", temperature=0, max_tokens=256)

    def _format_chat_context(self, chat_history: List[Dict]) -> str:
        """Format chat history into a context string for classification."""
        if not chat_history:
            return ""

        context = "Previous conversation:\n"
        for interaction in chat_history[-3:]:  # Use last 3 interactions
            context += f"Human: {interaction['query']}\n"
            context += f"Assistant: {interaction['response']}\n"
        context += "\nBased on this conversation context and the new question, "
        return context

    def classify_query(self, query: str, chat_history: List[Dict] = None) -> str:
        context = self._format_chat_context(chat_history) if chat_history else ""

        prompt = (
            f"{context}classify the following query into one of three categories: "
            f"if it was related to educational information about blockchain, give: {Config.BLOCKCHAIN_EDUCATOR_NAME},"
            f"if it was related to security stuff, give: {Config.CONTRACT_AUDITOR_NAME},"
            f"if it was related to transaction address analysis, give: {Config.TX_ADDRESS_ANALYZER_NAME}.\n"
            f"Query: {query}\nCategory:"
            f"Just return the category, no other text."
        )
        classification = self.llm(prompt)
        return classification
