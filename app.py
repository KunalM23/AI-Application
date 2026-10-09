import os
import requests
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

project_folder = Path(__file__).resolve().parent
load_dotenv(dotenv_path=project_folder / ".env", override=True)

try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

st.set_page_config(page_title="CrewAI RAG Scanner", layout="centered")

# Sidebar: Non-editable Route Display
st.sidebar.title("API Configuration")
st.sidebar.text_input(
    "Active FastAPI Endpoint (Read Only)",
    value="http://127.0.0.1:8000/ask",
    disabled=True
)

st.title("📄 AI Document Scanner (CrewAI + RAG)")
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
                endpoint = "http://127.0.0.1:8000/ask"
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {"question": question.strip()}

                response = requests.post(endpoint, files=files, data=data, timeout=180)
                result = response.json()

                if response.status_code == 200 and result.get("success"):
                    st.subheader("CrewAI Final Answer")
                    st.write(result["answer"])
                else:
                    st.error(result.get("detail", "Error running CrewAI execution."))
        except Exception as err:
            st.error(f"Could not connect to FastAPI server: {str(err)}")