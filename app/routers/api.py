# app/routers/api.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents import agents
from app.services import classifier

router = APIRouter()


class Query(BaseModel):
    query: str


@router.post("/query")
async def process_query(query: Query):
    classification = classifier.classify_query(query.query).lower()

    agent = agents.get(classification)
    if not agent:
        raise HTTPException(status_code=400, detail="Could not classify the query")

    response = agent.handle_query(query.query)
    return {"classification": classification, "response": response}
