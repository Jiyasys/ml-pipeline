# insights_feedback.py
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Literal, Optional

from fastapi import APIRouter, status
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger("edwiserr.insights")
router = APIRouter(tags=["insights"])

FeedbackLevel = Literal["strongly_resonates", "somewhat_resonates", "doesnt_feel_accurate"]
UserType = Literal["class_10", "class_12", "undergraduate", "postgraduate", "professional", "career_changer", "unknown"]


class OceanScores(BaseModel):
    Openness:          Optional[float] = Field(None, ge=0, le=100)
    Conscientiousness: Optional[float] = Field(None, ge=0, le=100)
    Extraversion:      Optional[float] = Field(None, ge=0, le=100)
    Agreeableness:     Optional[float] = Field(None, ge=0, le=100)
    Neuroticism:       Optional[float] = Field(None, ge=0, le=100)


class InsightFeedbackRequest(BaseModel):
    response_session_id: Optional[int] = None
    insight_id:          str  = Field(..., min_length=1, max_length=80)
    insight_title:       str  = Field(..., min_length=1, max_length=200)
    insight_text:        str  = Field(..., min_length=1, max_length=4000)
    feedback_level:      FeedbackLevel
    feedback_text:       Optional[str]        = Field(None, max_length=500)
    ocean_scores:        Optional[OceanScores] = None
    archetype_key:       Optional[str]        = Field(None, max_length=80)
    user_type:           Optional[UserType]   = None
    submitted_at:        Optional[datetime]   = None

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


def _resonance_category(level: FeedbackLevel) -> Literal["positive", "neutral", "negative"]:
    if level == "strongly_resonates": return "positive"
    if level == "somewhat_resonates": return "neutral"
    return "negative"


def _dominant_trait(scores: Optional[OceanScores]) -> Optional[str]:
    if not scores:
        return None
    values = {k: v for k, v in scores.model_dump().items() if v is not None}
    return max(values, key=lambda k: values[k]) if values else None


@router.post(
    "/feedback",
    response_model=InsightFeedbackResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def submit_insight_feedback(body: InsightFeedbackRequest) -> InsightFeedbackResponse:
    server_ts   = datetime.now(timezone.utc)
    feedback_id = f"{body.response_session_id}:{body.insight_id}"

    logger.info("[insight_feedback] session=%s insight=%s level=%s",
                body.response_session_id, body.insight_id, body.feedback_level)

    # Uncomment when Supabase is ready:
    # await supabase.table("insight_feedback").upsert({
    #     "feedback_id": feedback_id,
    #     "response_session_id": body.response_session_id,
    #     "insight_id": body.insight_id,
    #     "insight_title": body.insight_title,
    #     "feedback_level": body.feedback_level,
    #     "feedback_text": body.feedback_text,
    #     "ocean_scores": body.ocean_scores.model_dump() if body.ocean_scores else None,
    #     "archetype_key": body.archetype_key,
    #     "user_type": body.user_type,
    #     "created_at": server_ts.isoformat(),
    # }, on_conflict="feedback_id").execute()

    return InsightFeedbackResponse(
        status="accepted",
        feedback_id=feedback_id,
        insight_id=body.insight_id,
        feedback_level=body.feedback_level,
        server_timestamp=server_ts,
        analytics=AnalyticsSignals(
            resonance_category=_resonance_category(body.feedback_level),
            has_annotation=bool(body.feedback_text),
            ocean_dominant_trait=_dominant_trait(body.ocean_scores),
            archetype_key=body.archetype_key,
        ),
    )