"""
schemas.py
----------
Pydantic v2 schemas for EDWISERR.

Convention:
    <Model>Base     — shared field definitions
    <Model>Create   — used in POST request bodies (input)
    <Model>Update   — used in PATCH request bodies (partial update)
    <Model>Read     — returned in API responses (output)
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ─── Shared config ─────────────────────────────────────────────────────────────
class _OrmBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════════════════════════════════════
# School
# ══════════════════════════════════════════════════════════════════════════════
class SchoolBase(BaseModel):
    school_name: str = Field(..., min_length=1, max_length=255)
    test_link: str | None = Field(None, max_length=512)
    city: str | None = Field(None, max_length=100)
    state: str | None = Field(None, max_length=100)
    contact_person: str | None = Field(None, max_length=150)
    mobile: str | None = Field(None, max_length=20)


class SchoolCreate(SchoolBase):
    pass


class SchoolRead(_OrmBase, SchoolBase):
    id: int
    created_at: datetime


# ══════════════════════════════════════════════════════════════════════════════
# Test
# ══════════════════════════════════════════════════════════════════════════════
class TestBase(BaseModel):
    school_id: int
    title: str = Field(..., min_length=1, max_length=255)
    test_code: str = Field(..., min_length=1, max_length=64)
    is_active: bool = True


class TestCreate(TestBase):
    pass


class TestRead(_OrmBase, TestBase):
    id: int
    created_at: datetime


# ══════════════════════════════════════════════════════════════════════════════
# QuestionSet
# ══════════════════════════════════════════════════════════════════════════════
OCEAN_TRAITS = {"Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"}


class QuestionSetBase(BaseModel):
    question: str = Field(..., min_length=1)
    answer1: str = Field(..., min_length=1)
    answer2: str = Field(..., min_length=1)
    answer3: str = Field(..., min_length=1)
    answer4: str = Field(..., min_length=1)
    trait: str = Field(..., max_length=50)
    sub_dimension: str | None = Field(None, max_length=100)
    is_active: bool = True

    @field_validator("trait")
    @classmethod
    def trait_must_be_ocean(cls, v: str) -> str:
        if v not in OCEAN_TRAITS:
            raise ValueError(
                f"trait must be one of {sorted(OCEAN_TRAITS)}, got {v!r}"
            )
        return v


class QuestionSetCreate(QuestionSetBase):
    pass


class QuestionSetRead(_OrmBase, QuestionSetBase):
    id: int
    created_at: datetime


# ══════════════════════════════════════════════════════════════════════════════
# ResponseSession
# ══════════════════════════════════════════════════════════════════════════════
class ResponseSessionBase(BaseModel):
    school_id: int | None = None
    test_id: int | None = None
    student_identifier: str = Field(..., min_length=1, max_length=255)


class ResponseSessionCreate(ResponseSessionBase):
    pass


class ResponseSessionRead(_OrmBase, ResponseSessionBase):
    id: int
    started_at: datetime
    submitted_at: datetime | None


class ResponseSessionSubmit(BaseModel):
    """Marks a session as submitted (sets submitted_at timestamp)."""
    submitted_at: datetime


# ══════════════════════════════════════════════════════════════════════════════
# Response  (one row per answered question)
# ══════════════════════════════════════════════════════════════════════════════
class ResponseBase(BaseModel):
    response_session_id: int
    question_set_id: int
    selected_answer: str = Field(..., min_length=1, max_length=512)


class ResponseCreate(ResponseBase):
    pass


class ResponseRead(_OrmBase, ResponseBase):
    id: int
    created_at: datetime


# Batch submission — list of answers for an entire session
class ResponseBatchCreate(BaseModel):
    response_session_id: int
    answers: list[dict[str, Any]] = Field(
        ...,
        description="List of {question_set_id, selected_answer} objects",
        min_length=1,
    )

    @field_validator("answers")
    @classmethod
    def validate_answers(cls, v: list[dict]) -> list[dict]:
        for item in v:
            if "question_set_id" not in item or "selected_answer" not in item:
                raise ValueError(
                    "Each answer must contain 'question_set_id' and 'selected_answer'"
                )
            if not str(item["selected_answer"]).strip():
                raise ValueError("selected_answer cannot be blank")
        return v


# ══════════════════════════════════════════════════════════════════════════════
# InsightFeedback
# ══════════════════════════════════════════════════════════════════════════════
FEEDBACK_LEVELS = {
    "strongly_resonates",
    "resonates",
    "neutral",
    "does_not_resonate",
}


class InsightFeedbackCreate(BaseModel):
    response_session_id: int = Field(..., gt=0)
    insight_id: str = Field(..., min_length=1, max_length=100)
    insight_title: str = Field(..., min_length=1, max_length=255)
    insight_text: str = Field(..., min_length=1)
    feedback_level: str = Field(..., max_length=50)
    feedback_text: str | None = Field(None, max_length=2000)
    ocean_scores: dict[str, float | int] | None = None

    @field_validator("feedback_level")
    @classmethod
    def feedback_level_must_be_valid(cls, v: str) -> str:
        if v not in FEEDBACK_LEVELS:
            raise ValueError(
                f"feedback_level must be one of {sorted(FEEDBACK_LEVELS)}, got {v!r}"
            )
        return v

    @field_validator("ocean_scores")
    @classmethod
    def validate_ocean_scores(
        cls, v: dict[str, float | int] | None
    ) -> dict[str, float | int] | None:
        if v is None:
            return v
        allowed_keys = {
            "Openness",
            "Conscientiousness",
            "Extraversion",
            "Agreeableness",
            "Neuroticism",
        }
        unknown = set(v.keys()) - allowed_keys
        if unknown:
            raise ValueError(
                f"Unknown OCEAN keys: {unknown}. Allowed: {allowed_keys}"
            )
        for key, score in v.items():
            if not (0 <= float(score) <= 100):
                raise ValueError(f"Score for {key!r} must be between 0 and 100")
        return v


class InsightFeedbackRead(_OrmBase):
    id: int
    response_session_id: int
    insight_id: str
    insight_title: str
    insight_text: str
    feedback_level: str
    feedback_text: str | None
    ocean_scores: dict[str, float | int] | None
    created_at: datetime


# ─── Generic API response envelopes ───────────────────────────────────────────
class SuccessResponse(BaseModel):
    success: bool = True
    message: str


class ErrorDetail(BaseModel):
    field: str | None = None
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    errors: list[ErrorDetail]