from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_service import query_documents
from app.services.gemini_service import generate_response

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
async def chat(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    retrieved_chunks = query_documents(request.query, top_k=4)

    if not retrieved_chunks:
        return {
            "answer": "I don't have any documents to reference yet. Please upload a document first.",
            "sources": []
        }

    answer = generate_response(request.query, retrieved_chunks)
    sources = list(set(chunk["source"] for chunk in retrieved_chunks))

    return {
        "answer": answer,
        "sources": sources
    }