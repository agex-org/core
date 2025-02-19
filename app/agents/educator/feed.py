import glob
import os

import fitz
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

load_dotenv()


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text


def load_and_chunk_pdfs(pdf_files):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = []
    for pdf_file in pdf_files:
        extracted_text = extract_text_from_pdf(pdf_file)
        chunks = text_splitter.split_text(extracted_text)
        texts.extend(chunks)
    return texts


if os.getenv("FEED_EDUCATOR") == "False":
    print("Skipping PDF processing and embedding")
    exit()

print("Loading and chunking PDFs...")
base_path = os.path.dirname(os.path.abspath(__file__))
books_path = os.path.join(base_path, "books")
pdf_files = glob.glob(os.path.join(books_path, "*.pdf"))
print(f"Found {len(pdf_files)} PDFs in {books_path}")
documents = load_and_chunk_pdfs(pdf_files)
print(f"Loaded {len(documents)} documents")

# Use a local Hugging Face embedding model for generating embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
print("Embedding documents...")
vector_db = FAISS.from_texts(documents, embedding_model)
print("Vector database created")
print("Saving FAISS index...")
vector_db.save_local("faiss_index")
print("✅ PDFs processed and stored in FAISS!")
