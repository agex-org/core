from app.agents.auditor.feed import process_pdfs
from app.config import Config

if __name__ == "__main__":
    if Config.FEED_AUDITOR:
        process_pdfs(
            input_dir="app/agents/auditor/books",
            output_dir="faiss_index/auditor",
        )
    else:
        print("Skipping PDF processing and embedding")
