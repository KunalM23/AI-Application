import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from tools import search_vector_db

load_dotenv()

# Initialize Gemini LLM for CrewAI
gemini_llm = LLM(
    model="gemini-3.1-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY")
)

# Agent 1: RAG Search Expert
researcher_agent = Agent(
    role="Document RAG Specialist",
    goal="Retrieve accurate text context from the uploaded document for the user question.",
    backstory="You are an expert at searching document vector databases and extracting factual information.",
    tools=[search_vector_db],
    llm=gemini_llm,
    verbose=False
)

# Agent 2: Synthesis & QA Specialist
synthesizer_agent = Agent(
    role="Document QA Summarizer",
    goal="Synthesize retrieved context into a concise, direct answer.",
    backstory="You are a meticulous analyst who answers user questions using only provided document facts.",
    llm=gemini_llm,
    verbose=False
)