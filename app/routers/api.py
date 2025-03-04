# app/routers/history.py
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.agents import agents
from app.services import classifier, title_generator
from app.services.chat_history_service import ChatHistoryService

router = APIRouter()
chat_history_service = ChatHistoryService()


class Query(BaseModel):
    query: str


@router.post("/create")
async def create_session(request: Request):
    """
    Create a new chat session.
    """
    client_ip = request.client.host
    session_id = chat_history_service.create_session(client_ip)
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
        {"session_id": session.get("session_id"), "title": session.get("title")}
        for session in sessions
    ]
    return {"chat_history_list": session_ids}


@router.get("/history/{session_id}")
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
    Uses the classifier and corresponding agent to handle the query.
    """
    client_ip = request.client.host

    # Ensure the session exists by checking the sessions list
    sessions = chat_history_service.get_sessions(client_ip)
    session = next((s for s in sessions if s["session_id"] == session_id), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Get existing chat history for the session
    history = chat_history_service.get_history(client_ip, session_id)
    # Classify the query using the history context
    classification = classifier.classify_query(query.query, history).lower()
    agent = agents.get(classification)
    if not agent:
        raise HTTPException(status_code=404, detail="Could not classify the query")

    # Generate title if needed
    if not session.get("title") or session["title"] == "":
        generated_title = title_generator.generate(query.query).strip()
        if generated_title:  # Only update if generator gave us something non-empty
            chat_history_service.update_session_title(
                client_ip, session_id, generated_title
            )
        session_title = generated_title
    else:
        session_title = session.get("title")

    # Process the query and get a response
    response = agent().handle_query(query.query, history)
    # Add the new interaction to the session's history
    updated_history = chat_history_service.add_interaction(
        client_ip=client_ip,
        session_id=session_id,
        query=query.query,
        classification=classification,
        response=response,
    )
    return {
        "title": session_title,
        "classification": classification,
        "response": response,
        "history": updated_history,
    }
