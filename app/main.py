from fastapi import FastAPI, Depends
from app.config import DEBUG_MODE
from app.schemas import Question
from app.services.retrieval import retrieve
from app.services.llm import ask_llm
from app.security import get_current_role


app = FastAPI(title="HR RAG BOT")
@app.get("/health")
def health():
    return ("status ok")

@app.post("/ask")
def ask_rag(
    data: Question,
    role: str = Depends(get_current_role)
    ):
    
    context = retrieve(
        query=data.question,
        user_role=role
        )
    answer = ask_llm(
        question=data.question,
        context=context
        )

    return {
        "role": role,
        "question": data.question,
        "answer": answer
    }


