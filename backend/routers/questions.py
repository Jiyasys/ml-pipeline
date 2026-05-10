"""
routers/questions.py
--------------------
OCEAN question bank management endpoints.
"""

from __future__ import annotations

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud.crud import create_question, get_question, list_questions
from db.deps import get_db
from models.models import QuestionSet
from schemas.schemas import QuestionSetCreate, QuestionSetRead

router = APIRouter(
    prefix="/api/v1/questions",
    tags=["Question Bank"],
)


@router.post(
    "",
    response_model=QuestionSetRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a question to the OCEAN bank",
)
def add_question(
    payload: QuestionSetCreate,
    db: Session = Depends(get_db),
) -> QuestionSet:
    return create_question(db, payload)


@router.get(
    "",
    response_model=list[QuestionSetRead],
    summary="List OCEAN questions (optionally filter by trait)",
)
def get_questions(
    trait: str | None = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
) -> Sequence[QuestionSet]:
    return list_questions(db, trait=trait, active_only=active_only, skip=skip, limit=limit)


@router.get(
    "/{question_id}",
    response_model=QuestionSetRead,
    summary="Get a question by ID",
)
def get_question_by_id(
    question_id: int,
    db: Session = Depends(get_db),
) -> QuestionSet:
    q = get_question(db, question_id)
    if q is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question id={question_id} not found.",
        )
    return q