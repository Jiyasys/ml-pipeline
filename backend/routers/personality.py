# ============================================================
# EDWISERR — Personality Router (FastAPI)
# POST /api/personality/questions  → adaptive question set
# POST /api/personality/submit     → answers + timing → profile
# POST /api/personality/clarify    → 2 clarification questions
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel, field_validator
from typing import Dict, Literal, Optional

from personality.scorer   import build_profile
from personality.selector import select_questions, select_clarification_questions

router = APIRouter()

# ── Models ───────────────────────────────────────────────────

class QuestionRequest(BaseModel):
    user_type: Literal['class_10', 'class_12', 'undergraduate', 'professional']
    inst_id:   str
    mode:      Literal['fast', 'standard', 'full'] = 'standard'
    seed:      Optional[int] = None

class AnswerSubmission(BaseModel):
    user_type:         Literal['class_10', 'class_12', 'undergraduate', 'professional']
    inst_id:           str
    answers:           Dict[str, Literal['A', 'B', 'C', 'D']]
    response_times_ms: Optional[Dict[str, int]] = None

    @field_validator('answers')
    @classmethod
    def min_answers(cls, v):
        if len(v) < 5:
            raise ValueError('At least 5 answers required.')
        return v

class ClarifyRequest(BaseModel):
    ocean_scores:     Dict[str, float]
    existing_answers: Dict[str, str]

# ── Endpoints ────────────────────────────────────────────────

@router.post('/questions')
def get_questions(req: QuestionRequest):
    questions = select_questions(
        user_type=req.user_type,
        mode=req.mode,
        seed=req.seed,
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
        'user_type': req.user_type,
        'inst_id':   req.inst_id,
        'mode':      req.mode,
        'total':     len(clean),
        'questions': clean,
    }

@router.post('/submit')
def submit_answers(submission: AnswerSubmission):
    profile = build_profile(
        user_type         = submission.user_type,
        inst_id           = submission.inst_id,
        answers           = submission.answers,
        response_times_ms = submission.response_times_ms or {},
    )
    return profile

@router.post('/clarify')
def get_clarification(req: ClarifyRequest):
    questions = select_clarification_questions(
        ocean_scores     = req.ocean_scores,
        existing_answers = req.existing_answers,
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
    return {'clarification_questions': clean, 'count': len(clean)}