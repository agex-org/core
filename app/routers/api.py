# app/routers/history.py
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.agents.orchestrator import OrchestratorAgent
from app.services.chat_history_service import ChatHistoryService

router = APIRouter()
chat_history_service = ChatHistoryService()
orchestrator = OrchestratorAgent()


class CreateSession(BaseModel):
    title: str


class Query(BaseModel):
    query: str


@router.post("/create")
async def create_session(data: CreateSession, request: Request):
    """
    Create a new chat session with a title.
    Returns the newly generated session_id.
    """
    client_ip = request.client.host
    session_id = chat_history_service.create_session(client_ip, data.title)
    return {"session_id": session_id}


@router.get("/list")
async def list_sessions(request: Request):
    """
    Return a list of session IDs for the client.
    Example response: { "chat_history_list": ["763875", "874561", "123456"] }
    """
    client_ip = request.client.host
    sessions = chat_history_service.get_sessions(client_ip)
    # Return only the session ids (or you could return the full info if needed)
    session_ids = [
        {"session_id": session["session_id"], "title": session["title"]}
        for session in sessions
    ]
    return {"chat_history_list": session_ids}


@router.get("/{session_id}")
async def get_history(session_id: str, request: Request):
    client_ip = request.client.host

    # Check if the session exists in the sessions list
    sessions = chat_history_service.get_sessions(client_ip)
    if not any(session["session_id"] == session_id for session in sessions):
        raise HTTPException(status_code=404, detail="Session not found")

    """
    Get the chat history for a given session id.
    """
    history = chat_history_service.get_history(client_ip, session_id)
    return {"session_id": session_id, "history": history}


@router.post("/flush")
async def flush(request: Request):
    """
    Flush the chat history.
    """
    chat_history_service.flush()
    return {"message": "Chat history flushed"}


@router.post("/{session_id}/query")
async def process_query(session_id: str, query: Query, request: Request):
    """
    Process a query in the context of a specific session.
    Uses the orchestrator agent to handle the query.
    """
    client_ip = request.client.host

    # Ensure the session exists
    sessions = chat_history_service.get_sessions(client_ip)
    if not any(session["session_id"] == session_id for session in sessions):
        raise HTTPException(status_code=404, detail="Session not found")

    # Get existing chat history
    history = chat_history_service.get_history(client_ip, session_id)

    # Use orchestrator agent to handle the query
    response = orchestrator.handle_query(query.query, history)

    # Add interaction to history
    updated_history = chat_history_service.add_interaction(
        client_ip=client_ip,
        session_id=session_id,
        query=query.query,
        classification="orchestrator",
        response=response,
    )

    return {
        "response": response,
        "history": updated_history,
    }
