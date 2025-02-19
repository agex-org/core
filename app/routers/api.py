# app/routers/api.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.agents import agents
from app.services import classifier
from app.services.chat_history_service import ChatHistoryService

router = APIRouter()
chat_history_service = ChatHistoryService()


class Query(BaseModel):
    query: str


@router.post("/query")
async def process_query(query: Query, request: Request):
    # Get client IP and chat history
    client_ip = request.client.host
    chat_history = chat_history_service.get_history(client_ip)

    # Process the query with chat history context
    classification = classifier.classify_query(query.query, chat_history).lower()
    agent = agents.get(classification)
    if not agent:
        raise HTTPException(status_code=200, detail="Could not classify the query")

    # Pass chat history to agent
    response = agent.handle_query(query.query, chat_history)

    # Store the interaction and get updated history
    chat_history = chat_history_service.add_interaction(
        client_ip=client_ip,
        query=query.query,
        classification=classification,
        response=response,
    )

    return {
        "classification": classification,
        "response": response,
        "chat_history": chat_history,
    }


@router.get("/chat-history")
async def get_chat_history(request: Request):
    client_ip = request.client.host
    chat_history = chat_history_service.get_history(client_ip)
    return {"chat_history": chat_history}
