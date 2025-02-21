from app.agents.feed import FeedAgent
from app.config import Config

if __name__ == "__main__":
    if Config.FEED_EDUCATOR:
        FeedAgent().feed(
            input_dir="app/agents/educator/books",
            output_dir="faiss_index/educator",
        )
    else:
        print("Skipping PDF processing and embedding")
