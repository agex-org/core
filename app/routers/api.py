# app/routers/api.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.analyzer_agent import TxAddressAnalyzerAgent
from app.agents.auditor_agent import ContractAuditorAgent
from app.agents.educator_agent import BlockchainEducatorAgent
from app.config import Config
from app.services.classification_service import ClassificationService

router = APIRouter()


class Query(BaseModel):
    query: str


@router.post("/query")
async def process_query(query: Query):
    classifier = ClassificationService()
    classification = classifier.classify_query(query.query)

    if classification == Config.BLOCKCHAIN_EDUCATOR_NAME:
        agent = BlockchainEducatorAgent()
    elif classification == Config.CONTRACT_AUDITOR_NAME:
        agent = ContractAuditorAgent()
    elif classification == Config.TX_ADDRESS_ANALYZER_NAME:
        agent = TxAddressAnalyzerAgent()
    else:
        raise HTTPException(status_code=400, detail="Could not classify the query")

    response = agent.handle_query(query.query)
    return {"classification": classification, "response": response}
