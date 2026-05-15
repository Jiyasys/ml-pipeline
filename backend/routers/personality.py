# ============================================================
# EDWISERR — Personality Router (FastAPI)
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator, model_validator
from typing import Dict, Literal, Optional
import logging

from personality.scorer import build_profile
from personality.selector import (
    select_questions,
    select_clarification_questions,
)

router = APIRouter()
logger = logging.getLogger(__name__)

# ============================================================
# Constants
# ============================================================

TRAITS = frozenset({
    "Openness",
    "Conscientiousness",
    "Extraversion",
    "Agreeableness",
    "Neuroticism",
})

VALID_ANSWER_VALUES = frozenset({"A", "B", "C", "D"})

USER_TYPES = Literal[
    "class_10",
    "class_12",
    "undergraduate",
    "professional",
]

ASSESSMENT_MODES = Literal["fast", "standard", "full"]

# Minimum answers per mode
MIN_ANSWERS = {
    "fast":     20,   # 25 questions served, allow up to 5 skipped
    "standard": 40,
    "full":     100,
}

MAX_RESPONSE_TIME_MS = 30_000
MIN_RESPONSE_TIME_MS = 300

# All valid question IDs from the question bank
from personality.questions import QUESTIONS as _ALL_QUESTIONS
_ALL_VALID_IDS = frozenset(q["id"] for q in _ALL_QUESTIONS)


# ============================================================
# Request Models
# ============================================================

class QuestionRequest(BaseModel):
    user_type: USER_TYPES
    inst_id:   str
    mode:      ASSESSMENT_MODES = "fast"
    seed:      Optional[int]    = None   # None = random per session

    @field_validator("inst_id")
    @classmethod
    def validate_inst_id(cls, v):
        if not v or not v.strip():
            raise ValueError("inst_id cannot be empty")
        return v.strip()


class AnswerSubmission(BaseModel):
    user_type:         USER_TYPES
    inst_id:           str
    mode:              ASSESSMENT_MODES                    = "fast"
    answers:           Dict[str, Literal["A", "B", "C", "D"]]
    response_times_ms: Optional[Dict[str, int]]           = None

    @field_validator("inst_id")
    @classmethod
    def validate_inst_id(cls, v):
        if not v or not v.strip():
            raise ValueError("inst_id cannot be empty")
        return v.strip()

    @field_validator("answers")
    @classmethod
    def validate_answers(cls, v):
        if not v:
            raise ValueError("answers cannot be empty")

        # ✅ Only validate answer VALUES (A/B/C/D) and that IDs exist in bank
        # ✅ Do NOT validate against seed=42 — seed is random per session now
        unknown_ids = set(v.keys()) - _ALL_VALID_IDS
        if unknown_ids:
            raise ValueError(
                f"Answers contain question IDs not in the question bank: "
                f"{sorted(unknown_ids)}"
            )

        return v

    @field_validator("response_times_ms")
    @classmethod
    def validate_response_times(cls, v):
        if v is None:
            return v
        for qid, ms in v.items():
            if not isinstance(ms, int):
                raise ValueError(f"response_times_ms for {qid} must be integer")
            if ms < MIN_RESPONSE_TIME_MS:
                v[qid] = MIN_RESPONSE_TIME_MS
            if ms > MAX_RESPONSE_TIME_MS:
                v[qid] = MAX_RESPONSE_TIME_MS
        return v

    @model_validator(mode="after")
    def validate_submission(self):
        min_required = MIN_ANSWERS[self.mode]
        if len(self.answers) < min_required:
            raise ValueError(
                f"Minimum {min_required} answers required for "
                f"mode={self.mode}, got {len(self.answers)}"
            )
        return self


class ClarifyRequest(BaseModel):
    user_type:        USER_TYPES
    ocean_scores:     Dict[str, float]
    confidences:      Dict[str, float]
    existing_answers: Dict[str, Literal["A", "B", "C", "D"]]

    @field_validator("ocean_scores")
    @classmethod
    def validate_scores(cls, v):
        invalid = set(v.keys()) - TRAITS
        if invalid:
            raise ValueError(f"Invalid trait keys: {sorted(invalid)}")
        return v


# ============================================================
# Helpers
# ============================================================

def serialize_questions(questions: list) -> list:
    return [
        {
            "id":            q["id"],
            "trait":         q["trait"],
            "sub_dimension": q["sub_dimension"],
            "scenario":      q["scenario"],
            "option_A":      q["option_A"],
            "option_B":      q["option_B"],
            "option_C":      q["option_C"],
            "option_D":      q["option_D"],
        }
        for q in questions
    ]


# ============================================================
# Endpoints
# ============================================================

@router.post("/questions")
def get_questions(req: QuestionRequest):
    try:
        questions = select_questions(
            user_type=req.user_type,
            mode=req.mode,
            seed=req.seed,       # None = random, int = reproducible
        )
        return {
            "user_type": req.user_type,
            "inst_id":   req.inst_id,
            "mode":      req.mode,
            "total":     len(questions),
            "questions": serialize_questions(questions),
        }
    except Exception as e:
        logger.exception("Question generation failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit")
def submit_answers(submission: AnswerSubmission):
    try:
        profile = build_profile(
            user_type=submission.user_type,
            inst_id=submission.inst_id,
            answers=submission.answers,
            response_times_ms=(submission.response_times_ms or {}),
        )
        return profile
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.exception("Profile generation failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clarify")
def get_clarification(req: ClarifyRequest):
    try:
        questions = select_clarification_questions(
            confidence={"per_trait": req.confidences},
            existing_answers=req.existing_answers,
            n=2,
        )
        return {
            "clarification_questions": serialize_questions(questions),
            "count": len(questions),
        }
    except Exception as e:
        logger.exception("Clarification question generation failed")
        raise HTTPException(status_code=500, detail=str(e))