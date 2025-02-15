# app/services/classification_service.py

from langchain_openai import ChatOpenAI

from app.config import Config


class ClassificationService:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=Config.OPENAI_API_KEY,
            openai_api_base=Config.OPENAI_BASE_URL,
            model="gpt-4",
            temperature=0,
        )

    def classify_query(self, query: str) -> str:
        prompt = (
            f"Classify the following query into one of three categories: "
            f"if it was related to educational information about blockchain, give: {Config.BLOCKCHAIN_EDUCATOR_NAME},"
            f"if it was related to security stuff, give: {Config.CONTRACT_AUDITOR_NAME},"
            f"if it was related to transaction address analysis, give: {Config.TX_ADDRESS_ANALYZER_NAME}.\n"
            f"Query: {query}\nCategory:"
            f"Just return the category, no other text."
        )
        response = self.llm.invoke(
            input=prompt,
        )
        classification = response.content
        return classification
