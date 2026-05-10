# ============================================================
# EDWISERR — Personality Router (FastAPI)
# Stable MVP Version
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

MIN_ANSWERS = {
    "fast": 20,
    "standard": 50,
    "full": 150,
}

MAX_RESPONSE_TIME_MS = 30000
MIN_RESPONSE_TIME_MS = 300


# ============================================================
# Request Models
# ============================================================

class QuestionRequest(BaseModel):
    user_type: USER_TYPES
    inst_id: str
    mode: ASSESSMENT_MODES = "fast"
    seed: Optional[int] = 42

    @field_validator("inst_id")
    @classmethod
    def validate_inst_id(cls, v):
        if not v or not v.strip():
            raise ValueError("inst_id cannot be empty")
        return v.strip()


class AnswerSubmission(BaseModel):
    user_type: USER_TYPES
    inst_id: str
    mode: ASSESSMENT_MODES = "fast"

    answers: Dict[str, Literal["A", "B", "C", "D"]]

    response_times_ms: Optional[Dict[str, int]] = None

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

        for qid, ans in v.items():
            if ans not in VALID_ANSWER_VALUES:
                raise ValueError(
                    f"Invalid answer value for {qid}: {ans}"
                )

        return v

    @field_validator("response_times_ms")
    @classmethod
    def validate_response_times(cls, v):

        if v is None:
            return v

        for qid, ms in v.items():

            if not isinstance(ms, int):
                raise ValueError(
                    f"response_times_ms for {qid} must be integer"
                )

            # Ignore absurd outliers instead of crashing
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
                f"Minimum {min_required} answers required for mode={self.mode}"
            )

        served_questions = select_questions(
            user_type=self.user_type,
            mode=self.mode,
            seed=42,
        )

        served_ids = {
            q["id"] for q in served_questions
        }

        invalid_ids = (
            set(self.answers.keys()) - served_ids
        )

        if invalid_ids:
            raise ValueError(
                f"Unknown or invalid question IDs: {sorted(invalid_ids)}"
            )

        return self


class ClarifyRequest(BaseModel):

    user_type: USER_TYPES

    ocean_scores: Dict[str, float]

    confidences: Dict[str, float]

    existing_answers: Dict[
        str,
        Literal["A", "B", "C", "D"]
    ]

    @field_validator("ocean_scores")
    @classmethod
    def validate_scores(cls, v):

        invalid = set(v.keys()) - TRAITS

        if invalid:
            raise ValueError(
                f"Invalid trait keys: {sorted(invalid)}"
            )

        return v


# ============================================================
# Helpers
# ============================================================

def serialize_questions(questions):

    clean = []

    for q in questions:

        clean.append({
            "id": q["id"],
            "trait": q["trait"],
            "sub_dimension": q["sub_dimension"],
            "scenario": q["scenario"],
            "option_A": q["option_A"],
            "option_B": q["option_B"],
            "option_C": q["option_C"],
            "option_D": q["option_D"],
        })

    return clean


# ============================================================
# Endpoints
# ============================================================

@router.post("/questions")
def get_questions(req: QuestionRequest):

    try:

        questions = select_questions(
            user_type=req.user_type,
            mode=req.mode,
            seed=req.seed,
        )

        clean = serialize_questions(questions)

        return {
            "user_type": req.user_type,
            "inst_id": req.inst_id,
            "mode": req.mode,
            "total": len(clean),
            "questions": clean,
        }

    except Exception as e:

        logger.exception("Question generation failed")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.post("/submit")
def submit_answers(submission: AnswerSubmission):

    try:

        profile = build_profile(
            user_type=submission.user_type,
            inst_id=submission.inst_id,
            answers=submission.answers,
            response_times_ms=(
                submission.response_times_ms or {}
            ),
        )

        return profile

    except ValueError as e:

        raise HTTPException(
            status_code=422,
            detail=str(e),
        )

    except Exception as e:

        logger.exception("Profile generation failed")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.post("/clarify")
def get_clarification(req: ClarifyRequest):

    try:

        questions = (
            select_clarification_questions(
                user_type=req.user_type,
                ocean_scores=req.ocean_scores,
                confidences=req.confidences,
                existing_answers=req.existing_answers,
                n=2,
            )
        )

        clean = serialize_questions(questions)

        return {
            "clarification_questions": clean,
            "count": len(clean),
        }

    except Exception as e:

        logger.exception(
            "Clarification question generation failed"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )