# app/agents/educator_agent.py

import openai
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.config import Config


class BlockchainEducatorAgent:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        openai.base_url = Config.OPENAI_BASE_URL
        self.vector_store = FAISS.load_local(
            "faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True
        )
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,
            openai_api_key=Config.OPENAI_API_KEY,
            openai_api_base=Config.OPENAI_BASE_URL,
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
        )

    def handle_query(self, query: str) -> str:
        return self.qa_chain.invoke(query)
