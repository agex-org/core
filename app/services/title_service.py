from langchain_openai import ChatOpenAI

from app.config import Config


class TitleGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=Config.OPENAI_API_KEY,
            openai_api_base=Config.OPENAI_BASE_URL,
            model=Config.OPENAI_MODEL,
            temperature=0,
        )

    def generate(self, query: str) -> str:
        prompt = (
            "Generate a concise and descriptive title for the following query:\n"
            f"Query: {query}\n"
            "Title:"
        )
        try:
            response = self.llm.invoke(input=prompt)
            title = response.content.strip()
        except Exception as e:
            print(f"Error during title creation: {e}")
            title = "Untitled"
        return title
