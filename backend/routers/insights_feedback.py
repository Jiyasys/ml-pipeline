# routers/insights_feedback.py
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Literal, Optional

from fastapi import APIRouter, HTTPException, status
from db.client import get_supabase
from schemas.schemas import (
    AnalyticsSignals,
    FeedbackLevel,
    InsightFeedbackRequest,
    InsightFeedbackResponse,
    OceanScores,
)

logger = logging.getLogger("edwiserr.insights")
router = APIRouter(tags=["Insights"])


# ── Helpers (your original logic — untouched) ─────────────────────────────────
def _resonance_category(level: FeedbackLevel) -> Literal["positive", "neutral", "negative"]:
    if level == "strongly_resonates": return "positive"
    if level == "somewhat_resonates": return "neutral"
    return "negative"


def _dominant_trait(scores: Optional[OceanScores]) -> Optional[str]:
    if not scores:
        return None
    values = {k: v for k, v in scores.model_dump().items() if v is not None}
    return max(values, key=lambda k: values[k]) if values else None


# ── POST /insights/feedback ───────────────────────────────────────────────────
@router.post(
    "/insights/feedback",
    response_model=InsightFeedbackResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def submit_insight_feedback(body: InsightFeedbackRequest) -> InsightFeedbackResponse:
    sb        = get_supabase()
    server_ts = datetime.now(timezone.utc)

    # Verify session exists if one was provided
    if body.response_session_id is not None:
        check = (
            sb.table("response_sessions")
            .select("id")
            .eq("id", body.response_session_id)
            .maybe_single()
            .execute()
        )
        if not check.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ResponseSession id={body.response_session_id} not found.",
            )

    # Build the row to insert
    row = {
        "response_session_id": body.response_session_id,
        "insight_id":          body.insight_id,
        "insight_title":       body.insight_title,
        "insight_text":        body.insight_text,
        "feedback_level":      body.feedback_level,
        "feedback_text":       body.feedback_text,
        "ocean_scores":        (
            body.ocean_scores.model_dump(exclude_none=True)
            if body.ocean_scores else None
        ),
        "archetype_key":       body.archetype_key,
        "user_type":           body.user_type,
        "created_at":          server_ts.isoformat(),
    }

    # Remove None values so Supabase uses column defaults
    row = {k: v for k, v in row.items() if v is not None}

    res = sb.table("insight_feedback").insert(row).execute()

    if not res.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save feedback.",
        )

    feedback_id = f"{body.response_session_id}:{body.insight_id}"
    logger.info(
        "[insight_feedback] saved — id=%s insight=%s level=%s",
        res.data[0].get("id"), body.insight_id, body.feedback_level,
    )

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


# ── GET /insights/feedback/session/{session_id} ───────────────────────────────
@router.get("/insights/feedback/session/{session_id}")
def list_session_feedback(session_id: int) -> list[dict]:
    sb  = get_supabase()
    res = (
        sb.table("insight_feedback")
        .select("*")
        .eq("response_session_id", session_id)
        .execute()
    )
    return res.data


# ── GET /insights/feedback/insight/{insight_id} (analytics) ──────────────────
@router.get("/insights/feedback/insight/{insight_id}")
def list_insight_analytics(insight_id: str, limit: int = 500) -> list[dict]:
    sb  = get_supabase()
    res = (
        sb.table("insight_feedback")
        .select("*")
        .eq("insight_id", insight_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return res.data