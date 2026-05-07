# Corrected `routers/personality.py`
# ============================================================
# EDWISERR — Personality Router (FastAPI)
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator, model_validator
from typing import Dict, List, Literal, Optional
import logging

from personality.scorer import build_profile
from personality.selector import (
    select_questions,
    select_clarification_questions,
)
from personality.questions import get_question_ids_for_mode

router = APIRouter()
logger = logging.getLogger(__name__)


# ── Constants ────────────────────────────────────────────────

TRAITS = frozenset({
    'Openness',
    'Conscientiousness',
    'Extraversion',
    'Agreeableness',
    'Neuroticism',
})

VALID_ANSWER_VALUES = frozenset({'A', 'B', 'C', 'D'})

USER_TYPES = Literal[
    'class_10',
    'class_12',
    'undergraduate',
    'professional',
]

ASSESSMENT_MODES = Literal['fast', 'standard', 'full']

MIN_ANSWERS = {
    'fast': 20,
    'standard': 50,
    'full': 150,
}

MAX_RESPONSE_TIME_MS = 30000
MIN_RESPONSE_TIME_MS = 300



# ── Request Models ──────────────────────────────────────────

class QuestionRequest(BaseModel):
    user_type: USER_TYPES
    inst_id: str
    mode: ASSESSMENT_MODES = 'standard'
    seed: Optional[int] = 42

    @field_validator('inst_id')
    @classmethod
    def validate_inst_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('inst_id must not be empty.')
        return v.strip()


class QuestionOut(BaseModel):
    id: str
    scenario: str
    option_A: str
    option_B: str
    option_C: str
    option_D: str


class QuestionResponse(BaseModel):
    user_type: str
    inst_id: str
    mode: str
    total: int
    questions: List[QuestionOut]


class AnswerSubmission(BaseModel):
    user_type: USER_TYPES
    inst_id: str
    mode: ASSESSMENT_MODES = 'standard'

    answers: Dict[str, Literal['A', 'B', 'C', 'D']]
    response_times_ms: Optional[Dict[str, int]] = None

    @field_validator('inst_id')
    @classmethod
    def validate_inst_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('inst_id must not be empty.')
        return v.strip()

    @field_validator('answers')
    @classmethod
    def validate_answers(cls, v: dict) -> dict:
        if not v:
            raise ValueError('answers must not be empty.')

        for qid, answer in v.items():
            if not isinstance(qid, str) or not qid.strip():
                raise ValueError(f'Invalid question ID: {repr(qid)}')

            if answer not in VALID_ANSWER_VALUES:
                raise ValueError(
                    f'Invalid answer value for {qid}: {repr(answer)}'
                )

        return v

    @field_validator('response_times_ms')
    @classmethod
    def validate_response_times(cls, v: Optional[dict]) -> Optional[dict]:
        if v is None:
            return v

        for qid, ms in v.items():
            if not isinstance(qid, str) or not qid.strip():
                raise ValueError(f'Invalid timing question ID: {repr(qid)}')

            if not isinstance(ms, int):
                raise ValueError(
                    f'response_times_ms must contain integers. Got {repr(ms)}'
                )

            if ms < MIN_RESPONSE_TIME_MS or ms > MAX_RESPONSE_TIME_MS:
                raise ValueError(
                    f'response_times_ms for {qid} out of bounds: {ms}'
                )

        return v

    @model_validator(mode='after')
    def validate_submission(self):
        min_required = MIN_ANSWERS[self.mode]

        if len(self.answers) < min_required:
            raise ValueError(
                f'Minimum {min_required} answers required for mode={self.mode}'
            )

        # NOTE:
        # Exact session-bound validation should ideally compare against
        # the precise question IDs served to this specific assessment session.
        # Current validation ensures submitted IDs are valid for the
        # given user_type and mode.

        served_ids = get_question_ids_for_mode(
            user_type=self.user_type,
            mode=self.mode,
        )

        invalid_ids = set(self.answers.keys()) - served_ids

        if invalid_ids:
            raise ValueError(
                f'Unknown or invalid question IDs: {sorted(invalid_ids)}'
            )

        if self.response_times_ms:
            extra_timing_ids = (
                set(self.response_times_ms.keys()) - set(self.answers.keys())
            )

            if extra_timing_ids:
                raise ValueError(
                    f'Timing IDs missing in answers: {sorted(extra_timing_ids)}'
                )

        return self


class ClarifyRequest(BaseModel):
    user_type: USER_TYPES

    ocean_scores: Dict[str, float]
    confidences: Dict[str, float]

    existing_answers: Dict[str, Literal['A', 'B', 'C', 'D']]

    @field_validator('ocean_scores')
    @classmethod
    def validate_ocean_scores(cls, v: dict) -> dict:

        invalid = set(v.keys()) - TRAITS
        missing = TRAITS - set(v.keys())

        if invalid:
            raise ValueError(
                f'Invalid ocean trait keys: {sorted(invalid)}'
            )

        if missing:
            raise ValueError(
                f'Missing ocean trait keys: {sorted(missing)}'
            )

        for trait, score in v.items():
            if not isinstance(score, (int, float)):
                raise ValueError(
                    f'{trait} must be numeric.'
                )

            if score < 0 or score > 100:
                raise ValueError(
                    f'{trait} must be between 0 and 100.'
                )

        return v

    @field_validator('confidences')
    @classmethod
    def validate_confidences(cls, v: dict) -> dict:

        invalid = set(v.keys()) - TRAITS
        missing = TRAITS - set(v.keys())

        if invalid:
            raise ValueError(
                f'Invalid confidence trait keys: {sorted(invalid)}'
            )

        if missing:
            raise ValueError(
                f'Missing confidence trait keys: {sorted(missing)}'
            )

        for trait, conf in v.items():
            if not isinstance(conf, (int, float)):
                raise ValueError(
                    f'{trait} confidence must be numeric.'
                )

            if conf < 0 or conf > 1:
                raise ValueError(
                    f'{trait} confidence must be between 0 and 1.'
                )

        return v


class TraitConfidence(BaseModel):
    Openness: float
    Conscientiousness: float
    Extraversion: float
    Agreeableness: float
    Neuroticism: float
    overall: float


class OceanScores(BaseModel):
    Openness: float
    Conscientiousness: float
    Extraversion: float
    Agreeableness: float
    Neuroticism: float


class PersonalityProfileResponse(BaseModel):
    ocean_scores: OceanScores
    confidence: TraitConfidence
    dominant_traits: List[str]
    low_traits: List[str]


class ClarifyResponse(BaseModel):
    clarification_questions: List[QuestionOut]
    count: int


# ── Helpers ─────────────────────────────────────────────────


def serialize_questions(questions: list) -> List[QuestionOut]:

    return [
        QuestionOut(
            id=q['id'],
            scenario=q['scenario'],
            option_A=q['option_A'],
            option_B=q['option_B'],
            option_C=q['option_C'],
            option_D=q['option_D'],
        )
        for q in questions
    ]


# ── Endpoints ───────────────────────────────────────────────

@router.post('/questions', response_model=QuestionResponse)
def get_questions(req: QuestionRequest):

    try:
        questions = select_questions(
            user_type=req.user_type,
            mode=req.mode,
            seed=req.seed,
        )

        serialized = serialize_questions(questions)

        return QuestionResponse(
            user_type=req.user_type,
            inst_id=req.inst_id,
            mode=req.mode,
            total=len(serialized),
            questions=serialized,
        )

    except ValueError as exc:
        logger.warning(f'Question validation failed: {exc}')
        raise HTTPException(status_code=422, detail=str(exc))

    except Exception:
        logger.exception('Question retrieval failed.')
        raise HTTPException(
            status_code=500,
            detail='Failed to retrieve assessment questions.'
        )


@router.post('/submit', response_model=PersonalityProfileResponse)
def submit_answers(submission: AnswerSubmission):

    try:
        profile = build_profile(
            user_type=submission.user_type,
            inst_id=submission.inst_id,
            answers=submission.answers,
            response_times_ms=submission.response_times_ms or {},
        )

        return profile

    except ValueError as exc:
        logger.warning(f'Profile build validation failed: {exc}')
        raise HTTPException(status_code=422, detail=str(exc))

    except Exception:
        logger.exception('Profile build failed.')
        raise HTTPException(
            status_code=500,
            detail='Failed to generate personality profile.'
        )


@router.post('/clarify', response_model=ClarifyResponse)
def get_clarification(req: ClarifyRequest):

    try:
        questions = select_clarification_questions(
            user_type=req.user_type,
            ocean_scores=req.ocean_scores,
            confidences=req.confidences,
            existing_answers=req.existing_answers,
            n=2,
        )

        serialized = serialize_questions(questions)

        return ClarifyResponse(
            clarification_questions=serialized,
            count=len(serialized),
        )

    except ValueError as exc:
        logger.warning(f'Clarification validation failed: {exc}')
        raise HTTPException(status_code=422, detail=str(exc))

    except Exception:
        logger.exception('Clarification retrieval failed.')
        raise HTTPException(
            status_code=500,
            detail='Failed to retrieve clarification questions.'
        )

