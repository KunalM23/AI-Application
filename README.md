# AI Multi-Agent Document Scanner and RAG System

An intelligent, multi-agent document analysis system built with CrewAI, FastAPI, Streamlit, and Google Gemini.

This application parses uploaded documents (PDF, DOCX, TXT, CSV, XLSX), generates vector embeddings using Google Gemini Embeddings (gemini-embedding-001), indexes them into an in-memory FAISS vector database, and executes a multi-agent retrieval workflow to provide precise, context-based answers.

## Tech Stack

- AI Framework: CrewAI (v1.15.22)
- LLM and Embeddings: Google Gemini (gemini-2.5-flash and models/gemini-embedding-001)
- Backend API: FastAPI and Uvicorn
- Frontend UI: Streamlit
- Vector Search: FAISS (faiss-cpu)
- Document Extractors: pypdf, python-docx, pandas, openpyxl

## Repository Structure

AI_Document_Scanner/
├── .env                # API Key configuration
├── .gitignore          # Excluded files and folders
├── requirements.txt    # Project dependencies
├── tools.py            # Text extraction and Gemini FAISS vector search tool
├── agents.py           # CrewAI Multi-Agent configurations
├── tasks.py            # CrewAI Task specifications
├── api.py              # FastAPI server handling crew operations
├── app.py              # Streamlit interactive user interface
└── README.md           # Project documentation

## Features

1. Multi-Format Document Processing: Supports PDF, Word documents (.docx), text files (.txt), and spreadsheets (.csv, .xlsx).
2. Multi-Agent Collaboration:
   - Document RAG Specialist: Executes semantic searches over the FAISS vector database.
   - Document QA Summarizer: Synthesizes facts retrieved from search results to compose accurate answers.
3. Decoupled Architecture: FastAPI backend processes multi-agent workflows, serving a lightweight Streamlit frontend.
4. Interactive UI: Streamlit web interface featuring an unmodifiable active route status indicator in the sidebar.

## Local Setup and Installation

### 1. Clone the Repository

git clone https://github.com/KunalM23/AI-Application.git
cd AI-Application

### 2. Create Virtual Environment and Install Dependencies

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

### 3. Environment Variable Configuration

Create a .env file in the root directory:

GEMINI_API_KEY=your_actual_gemini_api_key_here

## Running the Application

### Terminal 1: Start FastAPI Backend

uvicorn api:app --reload --port 8000

FastAPI server will be running at http://127.0.0.1:8000

### Terminal 2: Start Streamlit Frontend

streamlit run app.py

Streamlit UI will automatically open at http://localhost:8501

## Cloud Deployment (Streamlit Community Cloud)

1. Push this repository to GitHub.
2. Sign in to share.streamlit.io.
3. Create a new application referencing repo KunalM23/AI-Application, branch main, and main file app.py.
4. Add your API key under Advanced Settings > Secrets:

   GEMINI_API_KEY = "your_actual_gemini_api_key_here"

5. Click Deploy.
