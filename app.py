import os
import sys
import time
import requests
import subprocess
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
project_folder = Path(__file__).resolve().parent
load_dotenv(dotenv_path=project_folder / ".env", override=True)

# Fetch Gemini API key from Streamlit secrets if deployed
try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass


# Start FastAPI background process if running on Cloud or if server isn't active
@st.cache_resource
def ensure_fastapi_server_running(host: str = "127.0.0.1", port: int = 8000):
    """Ensures FastAPI is running in the background for Streamlit Cloud or standalone execution."""
    try:
        # Check if the server is already reachable
        requests.get(f"http://{host}:{port}/docs", timeout=1)
    except Exception:
        # If not reachable, launch FastAPI via Uvicorn in a background process
        cmd = [sys.executable, "-m", "uvicorn", "api:app", "--host", host, "--port", str(port)]
        subprocess.Popen(cmd)
        time.sleep(3)  # Allow Uvicorn time to initialize


st.set_page_config(page_title="CrewAI RAG Scanner", layout="centered")

# Sidebar: Flexible configuration for forks and local running
st.sidebar.title("API Configuration")

# Allow option to toggle custom server or use local auto-start
use_custom_endpoint = st.sidebar.checkbox("Use Custom API Endpoint", value=False)

if use_custom_endpoint:
    endpoint_url = st.sidebar.text_input(
        "FastAPI Endpoint URL",
        value="http://127.0.0.1:8000/ask",
        help="Enter your custom FastAPI backend URL if hosted separately."
    )
else:
    endpoint_url = "http://127.0.0.1:8000/ask"
    st.sidebar.text_input(
        "Active FastAPI Endpoint (Read Only)",
        value=endpoint_url,
        disabled=True
    )
    # Ensure FastAPI is running locally/in container background
    ensure_fastapi_server_running()

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
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {"question": question.strip()}

                response = requests.post(endpoint_url, files=files, data=data, timeout=180)
                result = response.json()

                if response.status_code == 200 and result.get("success"):
                    st.subheader("CrewAI Final Answer")
                    st.write(result["answer"])
                else:
                    st.error(result.get("detail", "Error running CrewAI execution."))
        except Exception as err:
            st.error(f"Could not connect to FastAPI server at {endpoint_url}: {str(err)}")