# app/agents/educator_agent.py

from langchain.agents import AgentType, initialize_agent
from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.agents.base import BaseAgent
from app.config import Config


class BlockchainEducatorAgent(BaseAgent):
    def __init__(self):
        # initialize qa tool
        self.llm = ChatOpenAI(
            openai_api_key=Config.OPENAI_API_KEY,
            openai_api_base=Config.OPENAI_BASE_URL,
            model=Config.OPENAI_MODEL,
            temperature=0,
        )
        self.vector_store = FAISS.load_local(
            "faiss_index/educator",
            OpenAIEmbeddings(),
            allow_dangerous_deserialization=True,
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

        # Initialize search tool
        search = DuckDuckGoSearchAPIWrapper()
        self.search_tool = Tool(
            name="Web Search",
            func=search.run,
            description="Useful for searching the internet for recent or additional information",
        )

        # Initialize agent with both QA and search capabilities
        tools = [self.qa_tool, self.search_tool]

        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )
        self.agent.handle_parsing_errors = True
