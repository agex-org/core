from langchain.agents import AgentType, initialize_agent
from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.agents.base import BaseAgent
from app.config import Config
from app.services.contract_code_retriever_service import ContractCodeRetriever


class ContractAuditorAgent(BaseAgent):
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(
            openai_api_key=Config.OPENAI_API_KEY,
            openai_api_base=Config.OPENAI_BASE_URL,
            model=Config.OPENAI_MODEL,
            temperature=0,
        )

        # initialize vector store for audit knowledge and qa chain and analyze contract tool
        self.vector_store = FAISS.load_local(
            "faiss_index/auditor",
            OpenAIEmbeddings(),
            allow_dangerous_deserialization=True,
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
        )
        # initialize analyze contract tool
        self.analyze_contract_tool = Tool(
            name="Analyze Contract Code",
            func=self.analyze_contract,
            description="Analyzes the given smart contract code for common vulnerabilities and security issues",
        )

        # initialize search tool
        search = DuckDuckGoSearchAPIWrapper()
        self.search_tool = Tool(
            name="Web Search",
            func=search.run,
            description="Useful for finding information about specific contracts or recent vulnerabilities",
        )

        # Initialize contract code retriever and tool
        self.contract_code_retriever = ContractCodeRetriever(
            api_url=Config.SONICSCAN_API_URL,
            api_key=Config.SONICSCAN_API_KEY,
            llm=self.llm,
        )
        self.main_contract_code_tool = Tool(
            name="Get Main Contract Code",
            func=self.contract_code_retriever.get_main_contract_code,
            description="Retrieves the main contract source code given a contract address",
        )

        # initialize structure response tool
        self.structure_response_tool = Tool(
            name="Structure Final Response",
            func=self.structure_final_response,
            description="Structures the final response into a clear summary of contract vulnerabilities",
        )

        # Initialize agent with all tools excluding the qa_tool
        tools = [
            # self.analyze_contract_tool,
            self.search_tool,
            self.main_contract_code_tool,
            self.structure_response_tool,
        ]
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )
        self.agent.handle_parsing_errors = True

    def structure_final_response(self, analysis: str) -> str:
        """Structures the analysis into a clear vulnerability summary"""
        prompt = """Based on the contract analysis provided, create a simple and clear response that:
        1. States if the contract is vulnerable or appears secure
        2. Lists any identified vulnerabilities or security concerns
        3. Provides a brief explanation for each vulnerability

        Format the response in a concise way. If no vulnerabilities are found, clearly state that.
        
        Analysis to process:
        {analysis}
        """

        print(f"Structuring final response for analysis length: {len(analysis)}")
        try:
            structured_response = self.llm.invoke(prompt.format(analysis=analysis))
            print(f"Structured response: {structured_response.content}")
            return structured_response.content
        except Exception as e:
            message = f"Error in structure_final_response: {str(e)}"
            print(message)
            return message

    def analyze_contract(self, contract_code: str) -> str:
        """Analyzes contract code for vulnerabilities using the QA chain"""
        prompt = f"""Analyze this smart contract code for vulnerabilities:

        {contract_code}

        Focus on:
        1. Reentrancy vulnerabilities
        2. Access control issues
        3. Integer overflow/underflow
        4. Unchecked external calls
        5. Other common security concerns"""

        print(f"Analyzing contract: {prompt}")
        try:
            result = self.qa_chain.invoke(prompt)
            print(f"Analysis result: {result}")
            return result
        except Exception as e:
            message = f"Error in analyze_contract: {str(e)}"
            print(message)
            return message
