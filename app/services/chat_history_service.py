import json
from datetime import datetime
from typing import Dict, List

import redis

from app.config import Config


class ChatHistoryService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True
        )
        self.max_history = 10
        self.expiry_seconds = 24 * 60 * 60  # 24 hours

    def get_history(self, client_ip: str) -> List[Dict]:
        """Get chat history for a client IP."""
        chat_history = self.redis_client.get(f"chat_history:{client_ip}")
        if chat_history:
            return json.loads(chat_history)
        return []

    def add_interaction(
        self, client_ip: str, query: str, classification: str, response: str
    ) -> List[Dict]:
        """Add a new interaction to the chat history."""
        chat_history = self.get_history(client_ip)

        interaction = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "classification": classification,
            "response": response,
        }

        chat_history.append(interaction)
        if len(chat_history) > self.max_history:
            chat_history = chat_history[-self.max_history :]

        self.redis_client.setex(
            f"chat_history:{client_ip}", self.expiry_seconds, json.dumps(chat_history)
        )

        return chat_history
