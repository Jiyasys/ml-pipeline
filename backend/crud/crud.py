"""
crud.py
-------
Reusable CRUD helpers for all EDWISERR models.
All functions receive a SQLAlchemy Session and return ORM objects.
No business logic here — routers handle that.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.models import (
    InsightFeedback,
    QuestionSet,
    Response,
    ResponseSession,
    School,
    Test,
)
from schemas.schemas import (
    InsightFeedbackCreate,
    QuestionSetCreate,
    ResponseCreate,
    ResponseSessionCreate,
    SchoolCreate,
    TestCreate,
)


# ── helpers ───────────────────────────────────────────────────────────────────
def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ══════════════════════════════════════════════════════════════════════════════
# School CRUD
# ══════════════════════════════════════════════════════════════════════════════
def create_school(db: Session, payload: SchoolCreate) -> School:
    school = School(**payload.model_dump())
    db.add(school)
    db.commit()
    db.refresh(school)
    return school


def get_school(db: Session, school_id: int) -> School | None:
    return db.get(School, school_id)


def list_schools(db: Session, skip: int = 0, limit: int = 100) -> Sequence[School]:
    stmt = select(School).offset(skip).limit(limit).order_by(School.id)
    return db.scalars(stmt).all()


# ══════════════════════════════════════════════════════════════════════════════
# Test CRUD
# ══════════════════════════════════════════════════════════════════════════════
def create_test(db: Session, payload: TestCreate) -> Test:
    test = Test(**payload.model_dump())
    db.add(test)
    db.commit()
    db.refresh(test)
    return test


def get_test(db: Session, test_id: int) -> Test | None:
    return db.get(Test, test_id)


def get_test_by_code(db: Session, code: str) -> Test | None:
    stmt = select(Test).where(Test.test_code == code)
    return db.scalars(stmt).first()


def list_tests_for_school(
    db: Session, school_id: int, active_only: bool = True
) -> Sequence[Test]:
    stmt = select(Test).where(Test.school_id == school_id)
    if active_only:
        stmt = stmt.where(Test.is_active.is_(True))
    return db.scalars(stmt.order_by(Test.id)).all()


# ══════════════════════════════════════════════════════════════════════════════
# QuestionSet CRUD
# ══════════════════════════════════════════════════════════════════════════════
def create_question(db: Session, payload: QuestionSetCreate) -> QuestionSet:
    question = QuestionSet(**payload.model_dump())
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_question(db: Session, question_id: int) -> QuestionSet | None:
    return db.get(QuestionSet, question_id)


def list_questions(
    db: Session,
    trait: str | None = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 200,
) -> Sequence[QuestionSet]:
    stmt = select(QuestionSet)
    if trait:
        stmt = stmt.where(QuestionSet.trait == trait)
    if active_only:
        stmt = stmt.where(QuestionSet.is_active.is_(True))
    stmt = stmt.offset(skip).limit(limit).order_by(QuestionSet.id)
    return db.scalars(stmt).all()


# ══════════════════════════════════════════════════════════════════════════════
# ResponseSession CRUD
# ══════════════════════════════════════════════════════════════════════════════
def create_response_session(
    db: Session, payload: ResponseSessionCreate
) -> ResponseSession:
    session = ResponseSession(**payload.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_response_session(db: Session, session_id: int) -> ResponseSession | None:
    return db.get(ResponseSession, session_id)


def submit_response_session(
    db: Session, session_id: int
) -> ResponseSession | None:
    """Mark a session as submitted (idempotent)."""
    session = db.get(ResponseSession, session_id)
    if session and session.submitted_at is None:
        session.submitted_at = _utcnow()
        db.commit()
        db.refresh(session)
    return session


# ══════════════════════════════════════════════════════════════════════════════
# Response CRUD  (normalised — one row per answer)
# ══════════════════════════════════════════════════════════════════════════════
def create_response(db: Session, payload: ResponseCreate) -> Response:
    response = Response(**payload.model_dump())
    db.add(response)
    db.commit()
    db.refresh(response)
    return response


def bulk_create_responses(
    db: Session,
    session_id: int,
    answers: list[dict],
) -> list[Response]:
    """
    Insert many answers in a single transaction.
    Each dict must have: question_set_id (int), selected_answer (str).
    Skips duplicates (same session + question) by checking first.
    """
    existing_q_ids: set[int] = {
        r.question_set_id
        for r in db.scalars(
            select(Response.question_set_id).where(
                Response.response_session_id == session_id
            )
        ).all()
    }

    new_rows: list[Response] = []
    for item in answers:
        q_id = int(item["question_set_id"])
        if q_id in existing_q_ids:
            continue  # skip duplicate
        row = Response(
            response_session_id=session_id,
            question_set_id=q_id,
            selected_answer=str(item["selected_answer"]),
        )
        db.add(row)
        new_rows.append(row)
        existing_q_ids.add(q_id)

    db.commit()
    for row in new_rows:
        db.refresh(row)
    return new_rows


def list_responses_for_session(
    db: Session, session_id: int
) -> Sequence[Response]:
    stmt = (
        select(Response)
        .where(Response.response_session_id == session_id)
        .order_by(Response.id)
    )
    return db.scalars(stmt).all()


# ══════════════════════════════════════════════════════════════════════════════
# InsightFeedback CRUD
# ══════════════════════════════════════════════════════════════════════════════
def create_insight_feedback(
    db: Session, payload: InsightFeedbackCreate
) -> InsightFeedback:
    feedback = InsightFeedback(**payload.model_dump())
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


def get_insight_feedback(db: Session, feedback_id: int) -> InsightFeedback | None:
    return db.get(InsightFeedback, feedback_id)


def list_feedback_for_session(
    db: Session, session_id: int
) -> Sequence[InsightFeedback]:
    stmt = (
        select(InsightFeedback)
        .where(InsightFeedback.response_session_id == session_id)
        .order_by(InsightFeedback.id)
    )
    return db.scalars(stmt).all()


def list_feedback_by_insight(
    db: Session, insight_id: str, limit: int = 500
) -> Sequence[InsightFeedback]:
    """Fetch all feedback entries for a specific insight slug (analytics)."""
    stmt = (
        select(InsightFeedback)
        .where(InsightFeedback.insight_id == insight_id)
        .order_by(InsightFeedback.created_at.desc())
        .limit(limit)
    )
    return db.scalars(stmt).all()