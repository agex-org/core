from app.agents.feed import FeedAgent
from app.config import Config

if __name__ == "__main__":
    if Config.FEED_AUDITOR:
        FeedAgent().feed(
            input_dir="app/agents/auditor/books",
            output_dir="faiss_index/auditor",
        )
    else:
        print("Skipping PDF processing and embedding")
