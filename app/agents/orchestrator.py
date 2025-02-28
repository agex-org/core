from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

from app.agents import agents
from app.agents.base import BaseAgent
from app.config import Config


class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.llm = ChatOpenAI(
            openai_api_key=Config.OPENAI_API_KEY,
            openai_api_base=Config.OPENAI_BASE_URL,
            model=Config.OPENAI_MODEL,
        )

        # Create tools from other agents
        self.tools = []
        for name, agent_info in agents.items():
            agent_instance = agent_info["agent"]()
            tool = Tool(
                name=name,
                func=agent_instance.handle_query,
                description=agent_info["description"],
            )
            self.tools.append(tool)

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )
