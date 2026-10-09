import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from crewai import Crew, Process

from tools import extract_text
from agents import researcher_agent, synthesizer_agent
from tasks import create_rag_tasks

project_folder = Path(__file__).resolve().parent
load_dotenv(dotenv_path=project_folder / ".env", override=True)

app = FastAPI(title="CrewAI RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health():
    return {"status": "running"}

def run_crew_workflow(file_bytes: bytes, file_name: str, question: str) -> str:
    """Parses text and runs CrewAI multi-agent workflow."""
    doc_text = extract_text(file_bytes, file_name)
    tasks = create_rag_tasks(researcher_agent, synthesizer_agent, doc_text, question)

    crew = Crew(
        agents=[researcher_agent, synthesizer_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff()
    return str(result.raw)

@app.post("/ask")
async def ask_question(
    file: UploadFile = File(...),
    question: str = Form(...)
):
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is missing.")

    try:
        file_bytes = await file.read()
        
        answer = await asyncio.to_thread(
            run_crew_workflow, 
            file_bytes, 
            file.filename or "", 
            question.strip()
        )

        return {
            "success": True,
            "answer": answer
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        await file.close()