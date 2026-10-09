import io
import os
import pandas as pd
from pathlib import Path
from docx import Document
from pypdf import PdfReader
from crewai.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text(file_bytes: bytes, file_name: str) -> str:
    """Extracts text content from PDF, DOCX, TXT, CSV, or XLSX files."""
    extension = Path(file_name).suffix.lower()
    file_stream = io.BytesIO(file_bytes)
    text = ""

    if extension == ".pdf":
        reader = PdfReader(file_stream)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif extension == ".docx":
        doc = Document(file_stream)
        for p in doc.paragraphs:
            text += p.text + "\n"
    elif extension == ".txt":
        text = file_bytes.decode("utf-8")
    elif extension == ".csv":
        text = pd.read_csv(file_stream).to_string()
    elif extension in [".xlsx", ".xls"]:
        text = pd.read_excel(file_stream).to_string()
    else:
        raise ValueError("Unsupported file format.")

    if not text.strip():
        raise ValueError("No readable text found in document.")

    return text

@tool("Search Vector Document Store")
def search_vector_db(document_text: str, question: str) -> str:
    """
    Chunks document text and creates a vector store using Google Gemini embeddings
    to find top matching context sections.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_text(document_text)

    # Google Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        api_key=api_key
    )

    vector_store = FAISS.from_texts(chunks, embeddings)
    docs = vector_store.similarity_search(question, k=3)
    return "\n\n".join([doc.page_content for doc in docs])