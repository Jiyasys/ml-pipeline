"""
models.py
---------
Complete SQLAlchemy ORM models for EDWISERR.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TypeDecorator

# ✅ FIX 1: flat import — no leading dots
from db.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class JSONType(TypeDecorator):
    impl = Text
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Any) -> str | None:
        if value is None:
            return None
        return json.dumps(value, ensure_ascii=False)

    def process_result_value(self, value: str | None, dialect: Any) -> Any:
        if value is None:
            return None
        return json.loads(value)


# ══════════════════════════════════════════════════════════════════════════════
# 1. Schools
# ══════════════════════════════════════════════════════════════════════════════
class School(Base):
    __tablename__ = "schools"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    school_name: Mapped[str] = mapped_column(String(255), nullable=False)
    test_link: Mapped[str | None] = mapped_column(String(512), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    contact_person: Mapped[str | None] = mapped_column(String(150), nullable=True)
    mobile: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )

    tests: Mapped[list["Test"]] = relationship(
        "Test", back_populates="school", cascade="all, delete-orphan", lazy="select"
    )
    response_sessions: Mapped[list["ResponseSession"]] = relationship(
        "ResponseSession", back_populates="school", cascade="all, delete-orphan", lazy="select"
    )

    def __repr__(self) -> str:
        return f"<School id={self.id} name={self.school_name!r}>"


# ══════════════════════════════════════════════════════════════════════════════
# 2. Tests
# ══════════════════════════════════════════════════════════════════════════════
class Test(Base):
    __tablename__ = "tests"
    __table_args__ = (UniqueConstraint("test_code", name="uq_tests_test_code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    school_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    test_code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )

    school: Mapped["School"] = relationship("School", back_populates="tests")
    response_sessions: Mapped[list["ResponseSession"]] = relationship(
        "ResponseSession", back_populates="test", cascade="all, delete-orphan", lazy="select"
    )

    def __repr__(self) -> str:
        return f"<Test id={self.id} code={self.test_code!r} school_id={self.school_id}>"


# ══════════════════════════════════════════════════════════════════════════════
# 3. QuestionSets
# ══════════════════════════════════════════════════════════════════════════════
class QuestionSet(Base):
    __tablename__ = "question_sets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer1: Mapped[str] = mapped_column(Text, nullable=False)
    answer2: Mapped[str] = mapped_column(Text, nullable=False)
    answer3: Mapped[str] = mapped_column(Text, nullable=False)
    answer4: Mapped[str] = mapped_column(Text, nullable=False)
    trait: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    sub_dimension: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )

    responses: Mapped[list["Response"]] = relationship(
        "Response", back_populates="question_set", lazy="select"
    )

    def __repr__(self) -> str:
        return f"<QuestionSet id={self.id} trait={self.trait!r}>"


# ══════════════════════════════════════════════════════════════════════════════
# 4. ResponseSessions
# ══════════════════════════════════════════════════════════════════════════════
class ResponseSession(Base):
    __tablename__ = "response_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    school_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("schools.id", ondelete="SET NULL"), nullable=True, index=True
    )
    test_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("tests.id", ondelete="SET NULL"), nullable=True, index=True
    )
    student_identifier: Mapped[str] = mapped_column(String(255), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    school: Mapped["School | None"] = relationship("School", back_populates="response_sessions")
    test: Mapped["Test | None"] = relationship("Test", back_populates="response_sessions")
    responses: Mapped[list["Response"]] = relationship(
        "Response", back_populates="response_session", cascade="all, delete-orphan", lazy="select"
    )
    insight_feedbacks: Mapped[list["InsightFeedback"]] = relationship(
        "InsightFeedback", back_populates="response_session", cascade="all, delete-orphan", lazy="select"
    )

    def __repr__(self) -> str:
        return f"<ResponseSession id={self.id} student={self.student_identifier!r} test_id={self.test_id}>"


# ══════════════════════════════════════════════════════════════════════════════
# 5. Responses
# ══════════════════════════════════════════════════════════════════════════════
class Response(Base):
    __tablename__ = "responses"
    __table_args__ = (
        UniqueConstraint(
            "response_session_id", "question_set_id",
            name="uq_response_session_question"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    response_session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("response_sessions.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    question_set_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("question_sets.id", ondelete="RESTRICT"),
        nullable=False, index=True
    )
    selected_answer: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )

    response_session: Mapped["ResponseSession"] = relationship(
        "ResponseSession", back_populates="responses"
    )
    question_set: Mapped["QuestionSet"] = relationship(
        "QuestionSet", back_populates="responses"
    )

    def __repr__(self) -> str:
        return (
            f"<Response id={self.id} session_id={self.response_session_id} "
            f"question_id={self.question_set_id} answer={self.selected_answer!r}>"
        )


# ══════════════════════════════════════════════════════════════════════════════
# 6. InsightFeedback
# ══════════════════════════════════════════════════════════════════════════════
class InsightFeedback(Base):
    __tablename__ = "insight_feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # ✅ FIX 2: nullable=True — students can submit without a session
    response_session_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("response_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    insight_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    insight_title: Mapped[str] = mapped_column(String(255), nullable=False)
    insight_text: Mapped[str] = mapped_column(Text, nullable=False)
    feedback_level: Mapped[str] = mapped_column(String(50), nullable=False)
    feedback_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    ocean_scores: Mapped[dict | None] = mapped_column(JSONType, nullable=True)

    # ✅ FIX 3: added archetype_key and user_type — your router sends these
    archetype_key: Mapped[str | None] = mapped_column(String(80), nullable=True)
    user_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )

    # nullable relationship — session may not exist
    response_session: Mapped["ResponseSession | None"] = relationship(
        "ResponseSession", back_populates="insight_feedbacks"
    )

    def __repr__(self) -> str:
        return (
            f"<InsightFeedback id={self.id} "
            f"session_id={self.response_session_id} "
            f"insight={self.insight_id!r} "
            f"level={self.feedback_level!r}>"
        )