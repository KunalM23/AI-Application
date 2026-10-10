import os
import requests
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Direct import of backend execution logic
from api import run_crew_workflow

# Load environment variables
project_folder = Path(__file__).resolve().parent
load_dotenv(dotenv_path=project_folder / ".env", override=True)

# Fetch Gemini API key from Streamlit secrets if deployed
try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

st.set_page_config(page_title="CrewAI RAG Scanner", layout="centered")

# Sidebar: Flexible configuration for forks and local running
st.sidebar.title("API Configuration")

# Informational note guiding users about local vs cloud usage
st.sidebar.info(
    "**Note:** Check this option **only** if you are running the FastAPI server "
    "locally on your machine (`uvicorn api:app`). Leave unchecked for Streamlit Cloud deployment."
)

use_custom_endpoint = st.sidebar.checkbox("Use External FastAPI Endpoint", value=False)

if use_custom_endpoint:
    endpoint_url = st.sidebar.text_input(
        "FastAPI Endpoint URL",
        value="http://127.0.0.1:8000/ask",
        help="Enter an external FastAPI backend URL if running separately."
    )
else:
    endpoint_url = "Direct Import (In-Memory Engine)"
    st.sidebar.text_input(
        "Backend Execution Mode",
        value=endpoint_url,
        disabled=True
    )

st.title("AI Document Scanner (CrewAI + RAG)")
st.caption("Powered by Multi-Agent CrewAI, FastAPI, FAISS & Google Gemini")

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["pdf", "docx", "txt", "csv", "xlsx"]
)

question = st.text_input("Ask a question about your document:")

if st.button("Run Multi-Agent Crew"):
    if not uploaded_file:
        st.error("Please upload a file.")
    elif not question.strip():
        st.error("Please enter a question.")
    else:
        try:
            with st.spinner("CrewAI agents are working on your document..."):
                if use_custom_endpoint:
                    # External FastAPI network request
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {"question": question.strip()}
                    response = requests.post(endpoint_url, files=files, data=data, timeout=180)
                    result = response.json()
                    
                    if response.status_code == 200 and result.get("success"):
                        st.subheader("CrewAI Final Answer")
                        st.write(result["answer"])
                    else:
                        st.error(result.get("detail", "Error running CrewAI execution."))
                else:
                    # Direct in-memory execution for Streamlit Cloud
                    answer = run_crew_workflow(
                        file_bytes=uploaded_file.getvalue(),
                        file_name=uploaded_file.name,
                        question=question.strip()
                    )
                    st.subheader("CrewAI Final Answer")
                    st.write(answer)
        except Exception as err:
            st.error(f"Execution failed: {str(err)}")