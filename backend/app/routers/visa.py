from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.visa_service import answer_visa_question

router = APIRouter()


class VisaQuestionRequest(BaseModel):
    question: str


@router.post("/visa-qa")
async def visa_qa(request: VisaQuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    result = answer_visa_question(request.question)
    return result