import json

import requests
from langchain.agents import AgentType, initialize_agent
from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.config import Config


class ContractAuditorAgent:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(
            openai_api_key=Config.OPENAI_API_KEY,
            openai_api_base=Config.OPENAI_BASE_URL,
            model=Config.OPENAI_MODEL,
            temperature=0,
        )

        # Initialize vector store for audit knowledge
        self.vector_store = FAISS.load_local(
            "faiss_index/auditor",
            OpenAIEmbeddings(),
            allow_dangerous_deserialization=True,
        )

        # Create QA chain for audit knowledge
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
        )

        # Create tools
        self.qa_tool = Tool(
            name="Audit Knowledge Base",
            func=self.qa_chain.run,
            description="Useful for getting information about smart contract vulnerabilities and best practices",
        )

        search = DuckDuckGoSearchAPIWrapper()
        self.search_tool = Tool(
            name="Web Search",
            func=search.run,
            description="Useful for finding information about specific contracts or recent vulnerabilities",
        )

        self.contract_code_tool = Tool(
            name="Get Contract Code",
            func=self.get_contract_code,
            description="Retrieves the source code of a smart contract given its address",
        )

        # Initialize agent with all tools including Slither
        tools = [self.qa_tool, self.search_tool, self.contract_code_tools]
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

    def get_contract_code(address: str) -> dict:
        """Retrieves contract source code from Sonicscan API"""
        try:
            url = "https://api.sonicscan.org/api"
            params = {
                "module": "contract",
                "action": "getsourcecode",
                "address": address,
                "apikey": Config.SONICSCAN_API_KEY,
            }

            response = requests.get(url, params=params)
            data = response.json()

            if data["status"] == "1" and data["result"]:
                source_code = data["result"][0]
                if source_code["SourceCode"] == "":
                    return "Contract source code not verified on Sonicscan"
                raw_source_code = source_code["SourceCode"]
                cleaned_str = raw_source_code[1:-1]
                sources = json.loads(cleaned_str)
                sources = sources.get("sources", {})

                # Create a dictionary to store contract names and their source code
                contracts_dict = {}
                for path, content in sources.items():
                    contracts_dict[path] = content["content"]

                return contracts_dict
            else:
                return f"Error retrieving source code: {data.get('message', 'Unknown error')}"
        except Exception as e:
            return f"Error retrieving contract code: {str(e)}"
