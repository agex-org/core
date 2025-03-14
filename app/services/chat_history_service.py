# app/services/chat_history_service.py
import json
import uuid
from datetime import datetime
from typing import Dict, List

import redis

from app.config import Config


class ChatHistoryService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASSWORD,
            db=0,
            decode_responses=True,
        )
        self.max_history = 10

    def _session_key(self, client_ip: str, session_id: str) -> str:
        return f"chat_history:{client_ip}:{session_id}"

    def _sessions_list_key(self, client_ip: str) -> str:
        return f"chat_sessions:{client_ip}"

    def create_session(self, client_ip: str) -> str:
        """
        Create a new chat session for the client.
        A simple session_id is generated using a portion of a UUID.
        """
        session_id = str(uuid.uuid4().int)[:12]  # e.g. 123456789012
        session_info = {
            "session_id": session_id,
            "title": "",
            "created_at": datetime.utcnow().isoformat(),
        }
        sessions_list_key = self._sessions_list_key(client_ip)
        sessions = self.get_sessions(client_ip)
        sessions.append(session_info)
        self.redis_client.set(sessions_list_key, json.dumps(sessions))
        # Initialize an empty chat history for the new session.
        self.redis_client.set(
            self._session_key(client_ip, session_id),
            json.dumps([]),
        )
        return session_id

    def get_sessions(self, client_ip: str) -> List[Dict]:
        """Return a list of session infos (each with session_id and title)."""
        sessions_list_key = self._sessions_list_key(client_ip)
        sessions = self.redis_client.get(sessions_list_key)
        if sessions:
            return json.loads(sessions)
        return []

    def get_history(self, client_ip: str, session_id: str) -> List[Dict]:
        """Return the chat history for a given session id."""
        history_key = self._session_key(client_ip, session_id)
        chat_history = self.redis_client.get(history_key)
        if chat_history:
            return json.loads(chat_history)
        return []

    def add_interaction(
        self,
        client_ip: str,
        session_id: str,
        query: str,
        classification: str,
        response: str,
    ) -> List[Dict]:
        """Add a new interaction to the specified chat session."""
        history_key = self._session_key(client_ip, session_id)
        chat_history = self.get_history(client_ip, session_id)
        interaction = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "classification": classification,
            "response": response,
        }
        chat_history.append(interaction)
        if len(chat_history) > self.max_history:
            chat_history = chat_history[-self.max_history :]
        self.redis_client.set(history_key, json.dumps(chat_history))
        return chat_history

    def update_session_title(
        self, client_ip: str, session_id: str, new_title: str
    ) -> bool:
        """
        Update the title of an existing session.
        """
        sessions_list_key = self._sessions_list_key(client_ip)
        sessions = self.get_sessions(client_ip)

        for session in sessions:
            if session["session_id"] == session_id:
                session["title"] = new_title.strip('"')
                break
        else:
            # Session not found
            return False

        self.redis_client.set(sessions_list_key, json.dumps(sessions))
        return True

    def flush(self):
        self.redis_client.flushall()
        print("Redis flushed")
        return True
