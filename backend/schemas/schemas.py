# schemas/schemas.py
from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

# ── Shared types ──────────────────────────────────────────────────────────────
FeedbackLevel = Literal["strongly_resonates", "somewhat_resonates", "doesnt_feel_accurate"]
UserType      = Literal["class_10", "class_12", "undergraduate", "postgraduate",
                         "professional", "career_changer", "unknown"]
OceanTrait    = Literal["Openness", "Conscientiousness", "Extraversion",
                         "Agreeableness", "Neuroticism"]


# ══════════════════════════════════════════════════════════════════════════════
# Schools
# ══════════════════════════════════════════════════════════════════════════════
class SchoolCreate(BaseModel):
    school_name:    str            = Field(..., min_length=1, max_length=255)
    test_link:      Optional[str]  = None
    city:           Optional[str]  = None
    state:          Optional[str]  = None
    contact_person: Optional[str]  = None
    mobile:         Optional[str]  = None


class SchoolRead(SchoolCreate):
    id:         int
    created_at: datetime


# ══════════════════════════════════════════════════════════════════════════════
# Tests
# ══════════════════════════════════════════════════════════════════════════════
class TestCreate(BaseModel):
    school_id:  int
    title:      str  = Field(..., min_length=1, max_length=255)
    test_code:  str  = Field(..., min_length=1, max_length=64)
    is_active:  bool = True


class TestRead(TestCreate):
    id:         int
    created_at: datetime


# ══════════════════════════════════════════════════════════════════════════════
# Question Sets
# ══════════════════════════════════════════════════════════════════════════════
class QuestionSetCreate(BaseModel):
    question:      str            = Field(..., min_length=1)
    answer1:       str            = Field(..., min_length=1)
    answer2:       str            = Field(..., min_length=1)
    answer3:       str            = Field(..., min_length=1)
    answer4:       str            = Field(..., min_length=1)
    trait:         OceanTrait
    sub_dimension: Optional[str]  = None
    is_active:     bool           = True


class QuestionSetRead(QuestionSetCreate):
    id:         int
    created_at: datetime


# ══════════════════════════════════════════════════════════════════════════════
# Response Sessions
# ══════════════════════════════════════════════════════════════════════════════
class ResponseSessionCreate(BaseModel):
    school_id:          Optional[int] = None
    test_id:            Optional[int] = None
    student_identifier: str           = Field(..., min_length=1, max_length=255)


class ResponseSessionRead(ResponseSessionCreate):
    id:           int
    started_at:   datetime
    submitted_at: Optional[datetime] = None


# ══════════════════════════════════════════════════════════════════════════════
# Responses  (one row per answer)
# ══════════════════════════════════════════════════════════════════════════════
class ResponseCreate(BaseModel):
    question_set_id: int
    selected_answer: str = Field(..., min_length=1, max_length=512)


class ResponseBatchCreate(BaseModel):
    answers: list[ResponseCreate] = Field(..., min_length=1)


class ResponseRead(ResponseCreate):
    id:                  int
    response_session_id: int
    created_at:          datetime


# ══════════════════════════════════════════════════════════════════════════════
# Insight Feedback
# ══════════════════════════════════════════════════════════════════════════════
class OceanScores(BaseModel):
    Openness:          Optional[float] = Field(None, ge=0, le=100)
    Conscientiousness: Optional[float] = Field(None, ge=0, le=100)
    Extraversion:      Optional[float] = Field(None, ge=0, le=100)
    Agreeableness:     Optional[float] = Field(None, ge=0, le=100)
    Neuroticism:       Optional[float] = Field(None, ge=0, le=100)


class InsightFeedbackRequest(BaseModel):
    response_session_id: Optional[int]         = None
    insight_id:          str                   = Field(..., min_length=1, max_length=80)
    insight_title:       str                   = Field(..., min_length=1, max_length=200)
    insight_text:        str                   = Field(..., min_length=1, max_length=4000)
    feedback_level:      FeedbackLevel
    feedback_text:       Optional[str]         = Field(None, max_length=500)
    ocean_scores:        Optional[OceanScores] = None
    archetype_key:       Optional[str]         = Field(None, max_length=80)
    user_type:           Optional[UserType]    = None
    submitted_at:        Optional[datetime]    = None

    @field_validator("insight_id")
    @classmethod
    def slugify_id(cls, v: str) -> str:
        import re
        return re.sub(r"[^a-z0-9-]", "", v.lower().replace(" ", "-"))

    @field_validator("feedback_text")
    @classmethod
    def strip_text(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else None


class AnalyticsSignals(BaseModel):
    resonance_category:   Literal["positive", "neutral", "negative"]
    has_annotation:       bool
    ocean_dominant_trait: Optional[str]
    archetype_key:        Optional[str]


class InsightFeedbackResponse(BaseModel):
    status:           Literal["accepted"]
    feedback_id:      str
    insight_id:       str
    feedback_level:   FeedbackLevel
    server_timestamp: datetime
    analytics:        AnalyticsSignals