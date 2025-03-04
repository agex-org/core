from abc import ABC
from datetime import datetime

from langchain.agents import AgentExecutor


class BaseAgent(ABC):
    _instances = {}
    agent: AgentExecutor

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    def handle_query(self, query: str, chat_history: list = None) -> str:
        try:
            # Format chat history into context if available
            context = ""
            if chat_history and len(chat_history) > 0:
                context = "Previous conversation:\n"
                for interaction in chat_history[
                    -3:
                ]:  # Use last 3 interactions for context
                    context += f"Human: {interaction['query']}\nAssistant: {interaction['response']}\n"
                context += "\nCurrent question: "

            # Combine context and query
            full_query = f"{context}{query}" if context else query
            full_query += (
                f"\nCurrent time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

            response = self.agent.invoke(full_query)
            return response.get("output")
        except Exception as e:
            return f"An error occurred: {str(e)}"
