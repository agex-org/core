# app/agents/educator_agent.py

import json

import requests
from langchain.agents import AgentType, initialize_agent
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM
from langchain.tools import Tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from app.config import Config


class OllamaLLM(LLM):
    """
    A custom LangChain LLM wrapper for the Ollama API.
    """

    model_name: str = "llama2:7b"
    temperature: float = 0.0
    max_tokens: int = 256

    def __init__(
        self,
        model_name: str = None,
        temperature: float = 0.0,
        max_tokens: int = 256,
        **kwargs,
    ):
        super().__init__(**kwargs)  # Initialize Pydantic fields
        if model_name is not None:
            self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    @property
    def _llm_type(self) -> str:
        return "ollama"

    def _call(self, prompt: str, stop: list[str] = None) -> str:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "parameters": {
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            },
        }
        url = "http://localhost:11434/api/generate"
        response = requests.post(url, json=payload)
        response.raise_for_status()

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            # Fallback: Assume the first line is valid JSON.
            text = response.text.strip()
            first_line = text.splitlines()[0]
            result = json.loads(first_line)

        # Adjust response parsing based on your Ollama API's output format.
        if "message" in result and "content" in result["message"]:
            return result["message"]["content"]
        return result.get("output", "")


class BlockchainEducatorAgent:
    def __init__(self):
        # Replace ChatOpenAI with our OllamaLLM instance
        self.llm = OllamaLLM(model_name="llama2:7b", temperature=0, max_tokens=256)

        # Load the vector store as before
        self.vector_store = FAISS.load_local(
            "faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
        )
        self.qa_tool = Tool(
            name="Blockchain Knowledge Base",
            func=self.qa_chain.run,
            description="Useful for answering questions about blockchain concepts",
        )

        # Initialize the web search tool using DuckDuckGo
        search = DuckDuckGoSearchAPIWrapper()
        self.search_tool = Tool(
            name="Web Search",
            func=search.run,
            description="Useful for searching the internet for recent or additional information",
        )

        # Combine both tools into the agent
        tools = [self.qa_tool, self.search_tool]
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

    def handle_query(self, query: str, chat_history: list = None) -> str:
        try:
            # Format chat history as context if available
            context = ""
            if chat_history and len(chat_history) > 0:
                context = "Previous conversation:\n"
                for interaction in chat_history[-3:]:
                    context += f"Human: {interaction['query']}\nAssistant: {interaction['response']}\n"
                context += "\nCurrent question: "

            full_query = f"{context}{query}" if context else query
            response = self.agent.invoke(full_query)
            return response.get("output")
        except Exception as e:
            return f"An error occurred: {str(e)}"
