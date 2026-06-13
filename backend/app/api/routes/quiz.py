from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

from app.services.style_quiz_service import get_quiz_questions, score_quiz_answers

router = APIRouter(prefix="/quiz", tags=["quiz"])


class QuizSubmission(BaseModel):
    answers: Dict[str, str]


class QuizResult(BaseModel):
    archetypes: List[str]
    style_tags: List[str]
    query_styles: List[str]


@router.get("/metadata")
def metadata():
    return {"questions": get_quiz_questions()}


@router.post("/score", response_model=QuizResult)
def score_quiz(submission: QuizSubmission):
    result = score_quiz_answers(submission.answers)
    return result
