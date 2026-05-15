# routers/questions.py
from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException, status
from db.client import get_supabase
from schemas.schemas import QuestionSetCreate, QuestionSetRead

logger = logging.getLogger("edwiserr.questions")
router = APIRouter(tags=["Question Bank"])


@router.post("/questions", response_model=QuestionSetRead, status_code=status.HTTP_201_CREATED)
def create_question(payload: QuestionSetCreate) -> QuestionSetRead:
    sb  = get_supabase()
    res = sb.table("question_sets").insert(payload.model_dump(exclude_none=True)).execute()

    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create question.")

    return QuestionSetRead(**res.data[0])


@router.get("/questions", response_model=list[QuestionSetRead])
def list_questions(
    trait: str | None = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 200,
) -> list[QuestionSetRead]:
    sb    = get_supabase()
    query = sb.table("question_sets").select("*")

    if trait:
        query = query.eq("trait", trait)
    if active_only:
        query = query.eq("is_active", True)

    res = query.range(skip, skip + limit - 1).execute()
    return [QuestionSetRead(**r) for r in res.data]


@router.get("/questions/{question_id}", response_model=QuestionSetRead)
def get_question(question_id: int) -> QuestionSetRead:
    sb  = get_supabase()
    res = sb.table("question_sets").select("*").eq("id", question_id).maybe_single().execute()

    if not res.data:
        raise HTTPException(status_code=404, detail=f"Question id={question_id} not found.")

    return QuestionSetRead(**res.data)