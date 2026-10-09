from crewai import Task

def create_rag_tasks(researcher_agent, synthesizer_agent, document_text: str, question: str):
    
    research_task = Task(
        description=(
            f"Search the document vector database for relevant information.\n"
            f"Question: {question}\n"
            f"Document Text Context: {document_text[:2000]}..."
        ),
        expected_output="Relevant text snippets retrieved from the vector search.",
        agent=researcher_agent
    )

    synthesis_task = Task(
        description=(
            f"Review the search results and construct a clear, direct answer to the question: '{question}'.\n"
            f"Rules:\n"
            f"1. Rely strictly on facts from the retrieved document context.\n"
            f"2. If the answer cannot be found, output: 'I cannot find this information in the document.'"
        ),
        expected_output="A concise, factual final answer.",
        agent=synthesizer_agent
    )

    return [research_task, synthesis_task]