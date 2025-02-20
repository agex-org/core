from app.agents.educator.feed import process_pdfs
from app.config import Config

if __name__ == "__main__":
    if Config.FEED_EDUCATOR:
        process_pdfs(
            input_dir="app/agents/educator/books",
            output_dir="faiss_index/educator",
        )
    else:
        print("Skipping PDF processing and embedding")
