import os

from app.agents.feed import FeedAgent
from app.config import Config

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(current_dir, "books")
    if Config.FEED_EDUCATOR:
        FeedAgent().feed(
            input_dir=input_dir,
            output_dir="faiss_index/educator",
        )
    else:
        print("Skipping PDF processing and embedding")
