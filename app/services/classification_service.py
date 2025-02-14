# app/services/classification_service.py

import openai

from app.config import Config


class ClassificationService:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        openai.base_url = Config.OPENAI_BASE_URL

    def classify_query(self, query: str) -> str:
        prompt = (
            f"Classify the following query into one of three categories: "
            f"if it was related to educational information about blockchain, give: {Config.BLOCKCHAIN_EDUCATOR_NAME},"
            f"if it was related to security stuff, give: {Config.CONTRACT_AUDITOR_NAME},"
            f"if it was related to transaction address analysis, give: {Config.TX_ADDRESS_ANALYZER_NAME}.\n"
            f"Query: {query}\nCategory:"
            f"Just return the category, no other text."
        )
        response = openai.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        classification = response.choices[0].message.content.strip().lower()
        return classification
