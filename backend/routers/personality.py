# ============================================================
# EDWISERR — Personality Router (FastAPI)
# Endpoints:
#   POST /api/personality/questions  → get adaptive question set
#   POST /api/personality/submit     → submit answers, get OCEAN profile
#   POST /api/personality/clarify    → get 2 clarification questions
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import Dict, Literal, Optional

from personality.scorer   import build_profile, compute_ocean_scores, compute_confidence
from personality.selector import select_questions, select_clarification_questions

router = APIRouter()

# ── Request / Response Models ────────────────────────────────

class QuestionRequest(BaseModel):
    user_type: Literal['class_10', 'class_12', 'undergraduate', 'professional']
    inst_id:   str
    mode:      Literal['fast', 'standard', 'full'] = 'standard'
    seed:      Optional[int] = None

class AnswerSubmission(BaseModel):
    user_type: Literal['class_10', 'class_12', 'undergraduate', 'professional']
    inst_id:   str
    # answers: {question_id: chosen_option}  e.g. {"O1": "C", "ST1": "A"}
    answers:   Dict[str, Literal['A', 'B', 'C', 'D']]

    @field_validator('answers')
    @classmethod
    def min_answers(cls, v):
        if len(v) < 5:
            raise ValueError('At least 5 answers required to compute a profile.')
        return v

class ClarifyRequest(BaseModel):
    ocean_scores:     Dict[str, float]
    existing_answers: Dict[str, str]

# ── Endpoints ────────────────────────────────────────────────

@router.post('/questions')
def get_questions(req: QuestionRequest):
    """
    Returns the adaptive question set for this session.
    Each question has: id, trait, sub_dimension, scenario, option_A–D (text only).
    Weights are NOT sent to the frontend — they're backend-only.
    """
    questions = select_questions(
        user_type=req.user_type,
        mode=req.mode,
        seed=req.seed,
    )

    # Strip weights before sending to frontend
    clean_questions = [
        {
            'id':            q['id'],
            'trait':         q['trait'],
            'sub_dimension': q['sub_dimension'],
            'scenario':      q['scenario'],
            'option_A':      q['option_A'],
            'option_B':      q['option_B'],
            'option_C':      q['option_C'],
            'option_D':      q['option_D'],
        }
        for q in questions
    ]

    return {
        'user_type':  req.user_type,
        'inst_id':    req.inst_id,
        'mode':       req.mode,
        'total':      len(clean_questions),
        'questions':  clean_questions,
    }


@router.post('/submit')
def submit_answers(submission: AnswerSubmission):
    """
    Accepts answers as {question_id: 'A'/'B'/'C'/'D'}.
    Returns full OCEAN profile.
    """
    profile = build_profile(
        user_type=submission.user_type,
        inst_id=submission.inst_id,
        answers=submission.answers,
    )
    return profile


@router.post('/clarify')
def get_clarification(req: ClarifyRequest):
    """
    Returns 2 clarification questions for the most uncertain traits.
    Call this when profile confidence < 0.75.
    """
    questions = select_clarification_questions(
        ocean_scores=req.ocean_scores,
        existing_answers=req.existing_answers,
        n=2,
    )

    clean = [
        {
            'id':            q['id'],
            'trait':         q['trait'],
            'sub_dimension': q['sub_dimension'],
            'scenario':      q['scenario'],
            'option_A':      q['option_A'],
            'option_B':      q['option_B'],
            'option_C':      q['option_C'],
            'option_D':      q['option_D'],
        }
        for q in questions
    ]

    return {
        'clarification_questions': clean,
        'count': len(clean),
    }