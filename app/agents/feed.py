import glob
import os

import fitz
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

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


def process_pdfs(input_dir, output_dir):
    """
    Process PDFs from input directory and save embeddings to output directory.

    Args:
        input_dir (str): Directory containing PDF files to process
        output_dir (str): Directory where to save the FAISS index
    """
    print(f"Loading and chunking PDFs from {input_dir}...")
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    print(f"Found {len(pdf_files)} PDFs")

    if not pdf_files:
        print("No PDF files found in the input directory")
        return

    documents = load_and_chunk_pdfs(pdf_files)
    print(f"Loaded {len(documents)} documents")

    embedding_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    print("Embedding documents...")
    vector_db = FAISS.from_texts(documents, embedding_model)
    print("Vector database created")

    os.makedirs(output_dir, exist_ok=True)
    print(f"Saving FAISS index to {output_dir}...")
    vector_db.save_local(output_dir)
    print("✅ PDFs processed and stored in FAISS!")
