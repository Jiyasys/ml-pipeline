"""
scripts/seed_db.py
------------------
Example CRUD usage — demonstrates creating every model and submitting
insight feedback end-to-end. Run once to populate edwiserr.db with
sample data for local development.

Usage:
    python -m scripts.seed_db
    # or from project root:
    python scripts/seed_db.py
"""

from __future__ import annotations

import sys
import os

# Allow running from project root without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db.database import init_db, SessionLocal
from crud.crud import (
    create_school,
    create_test,
    create_question,
    create_response_session,
    bulk_create_responses,
    submit_response_session,
    create_insight_feedback,
    list_feedback_for_session,
    list_responses_for_session,
)
from schemas.schemas import (
    SchoolCreate,
    TestCreate,
    QuestionSetCreate,
    ResponseSessionCreate,
    ResponseBatchCreate,
    InsightFeedbackCreate,
)


def main() -> None:
    # ── 0. Initialise DB ──────────────────────────────────────────────────
    print("Initialising database …")
    init_db()

    db = SessionLocal()

    try:
        # ── 1. Create a School ────────────────────────────────────────────
        school = create_school(
            db,
            SchoolCreate(
                school_name="Delhi Public School — Bengaluru",
                test_link="https://edwiserr.com/test/dps-blr",
                city="Bengaluru",
                state="Karnataka",
                contact_person="Ms Priya Sharma",
                mobile="+91-9876543210",
            ),
        )
        print(f"✅  School created: {school}")

        # ── 2. Create a Test ──────────────────────────────────────────────
        test = create_test(
            db,
            TestCreate(
                school_id=school.id,
                title="Grade 10 OCEAN Assessment — 2025",
                test_code="DPS-BLR-G10-2025",
                is_active=True,
            ),
        )
        print(f"✅  Test created: {test}")

        # ── 3. Seed Question Bank ─────────────────────────────────────────
        q1 = create_question(
            db,
            QuestionSetCreate(
                question="I enjoy exploring new ideas and experiences.",
                answer1="Strongly Agree",
                answer2="Agree",
                answer3="Disagree",
                answer4="Strongly Disagree",
                trait="Openness",
                sub_dimension="Intellectual Curiosity",
            ),
        )
        q2 = create_question(
            db,
            QuestionSetCreate(
                question="I prefer to have a detailed plan before starting a project.",
                answer1="Strongly Agree",
                answer2="Agree",
                answer3="Disagree",
                answer4="Strongly Disagree",
                trait="Conscientiousness",
                sub_dimension="Orderliness",
            ),
        )
        q3 = create_question(
            db,
            QuestionSetCreate(
                question="I feel energised when I am around other people.",
                answer1="Strongly Agree",
                answer2="Agree",
                answer3="Disagree",
                answer4="Strongly Disagree",
                trait="Extraversion",
                sub_dimension="Sociability",
            ),
        )
        print(f"✅  Questions created: {q1}, {q2}, {q3}")

        # ── 4. Start a Response Session ───────────────────────────────────
        session = create_response_session(
            db,
            ResponseSessionCreate(
                school_id=school.id,
                test_id=test.id,
                student_identifier="student-anon-uuid-abc123",
            ),
        )
        print(f"✅  ResponseSession created: {session}")

        # ── 5. Submit Answers (batch — one row per answer) ─────────────────
        answers = bulk_create_responses(
            db,
            session_id=session.id,
            answers=[
                {"question_set_id": q1.id, "selected_answer": "Strongly Agree"},
                {"question_set_id": q2.id, "selected_answer": "Agree"},
                {"question_set_id": q3.id, "selected_answer": "Disagree"},
            ],
        )
        print(f"✅  Responses saved: {len(answers)} rows")
        for r in answers:
            print(f"   → {r}")

        # ── 6. Mark Session as Submitted ──────────────────────────────────
        session = submit_response_session(db, session.id)
        print(f"✅  Session submitted at: {session.submitted_at}")

        # ── 7. Submit Insight Feedback ─────────────────────────────────────
        feedback = create_insight_feedback(
            db,
            InsightFeedbackCreate(
                response_session_id=session.id,
                insight_id="context-fluency",
                insight_title="Context Fluency",
                insight_text=(
                    "You have a natural ability to read the room and adapt your "
                    "communication style to different audiences."
                ),
                feedback_level="strongly_resonates",
                feedback_text="This part felt incredibly accurate — I do this all the time.",
                ocean_scores={
                    "Openness": 72,
                    "Conscientiousness": 65,
                    "Extraversion": 58,
                    "Agreeableness": 48,
                    "Neuroticism": 30,
                },
            ),
        )
        print(f"✅  InsightFeedback saved: {feedback}")

        # ── 8. Verify saved rows ───────────────────────────────────────────
        print("\n── Verification ─────────────────────────────────────────────")
        saved_responses = list_responses_for_session(db, session.id)
        print(f"   Responses in DB for session {session.id}: {len(saved_responses)}")
        for r in saved_responses:
            print(f"     {r}")

        saved_feedback = list_feedback_for_session(db, session.id)
        print(f"   Feedback records in DB for session {session.id}: {len(saved_feedback)}")
        for f in saved_feedback:
            print(f"     {f}")
            print(f"     ocean_scores (deserialised): {f.ocean_scores}")

        print("\n🎉  Seed complete! edwiserr.db is populated.")

    finally:
        db.close()


if __name__ == "__main__":
    main()