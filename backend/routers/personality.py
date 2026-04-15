from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from personality.scorer import compute_ocean_scores, ocean_to_mbti
from personality.confidence import compute_confidence
from personality.questions import select_adaptive_questions, encode_responses

router = APIRouter()

class UserContext(BaseModel):
    user_type: str      # class_10 / class_12 / undergraduate / professional
    inst_id: str        # inst_001 / inst_002 / inst_003

class AnswerSubmission(BaseModel):
    user_type: str
    inst_id: str
    answers: Dict[str, int]   # {question_id: 1-5}

@router.post("/questions")
def get_questions(context: UserContext):
    """Returns the adaptive question set for this user type."""
    questions = select_adaptive_questions(context.user_type)
    return {
        "user_type": context.user_type,
        "inst_id": context.inst_id,
        "total": len(questions),
        "questions": questions
    }

@router.post("/submit")
def submit_answers(submission: AnswerSubmission):
    """Takes answers, returns full OCEAN profile."""
    questions = select_adaptive_questions(submission.user_type)
    encoded   = encode_responses(submission.answers)
    ocean     = compute_ocean_scores(encoded, questions)
    confidence= compute_confidence(encoded, questions)
    mbti      = ocean_to_mbti(ocean)

    return {
        "institution_id":      submission.inst_id,
        "user_type":           submission.user_type,
        "ocean_scores":        ocean,
        "mbti_display":        mbti,
        "confidence":          confidence,
        "needs_clarification": confidence["overall"] < 0.75,
        "profile_complete":    True
    }