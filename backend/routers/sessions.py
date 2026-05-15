# routers/sessions.py
from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from db.client import get_supabase
from schemas.schemas import (
    ResponseBatchCreate,
    ResponseRead,
    ResponseSessionCreate,
    ResponseSessionRead,
)

logger = logging.getLogger("edwiserr.sessions")
router = APIRouter(tags=["Response Sessions"])


# ── Start a session ───────────────────────────────────────────────────────────
@router.post("/sessions", response_model=ResponseSessionRead, status_code=status.HTTP_201_CREATED)
def start_session(payload: ResponseSessionCreate) -> ResponseSessionRead:
    sb  = get_supabase()
    res = sb.table("response_sessions").insert(payload.model_dump(exclude_none=True)).execute()

    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create session.")

    logger.info("Session started: id=%s", res.data[0].get("id"))
    return ResponseSessionRead(**res.data[0])


# ── Mark session as submitted ─────────────────────────────────────────────────
@router.post("/sessions/{session_id}/submit", response_model=ResponseSessionRead)
def submit_session(session_id: int) -> ResponseSessionRead:
    sb  = get_supabase()

    # Check session exists
    check = sb.table("response_sessions").select("id").eq("id", session_id).maybe_single().execute()
    if not check.data:
        raise HTTPException(status_code=404, detail=f"Session id={session_id} not found.")

    res = (
        sb.table("response_sessions")
        .update({"submitted_at": datetime.now(timezone.utc).isoformat()})
        .eq("id", session_id)
        .execute()
    )

    return ResponseSessionRead(**res.data[0])


# ── Batch submit answers (one row per answer) ─────────────────────────────────
@router.post("/sessions/{session_id}/answers",
             response_model=list[ResponseRead],
             status_code=status.HTTP_201_CREATED)
def submit_answers(session_id: int, payload: ResponseBatchCreate) -> list[ResponseRead]:
    sb = get_supabase()

    # Check session exists
    check = sb.table("response_sessions").select("id").eq("id", session_id).maybe_single().execute()
    if not check.data:
        raise HTTPException(status_code=404, detail=f"Session id={session_id} not found.")

    rows = [
        {
            "response_session_id": session_id,
            "question_set_id":     answer.question_set_id,
            "selected_answer":     answer.selected_answer,
        }
        for answer in payload.answers
    ]

    res = sb.table("responses").insert(rows).execute()

    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to save answers.")

    logger.info("Saved %d answers for session %d", len(res.data), session_id)
    return [ResponseRead(**r) for r in res.data]


# ── Get all answers for a session ─────────────────────────────────────────────
@router.get("/sessions/{session_id}/answers", response_model=list[ResponseRead])
def get_answers(session_id: int) -> list[ResponseRead]:
    sb  = get_supabase()
    res = sb.table("responses").select("*").eq("response_session_id", session_id).execute()
    return [ResponseRead(**r) for r in res.data]