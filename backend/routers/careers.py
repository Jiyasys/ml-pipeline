# ============================================================
# EDWISERR — Careers Router (FastAPI)
# Prefix : /api/v1/careers
#
# POST /recommend          → top career matches
# POST /{career_id}        → single career detail
# GET  /categories         → available categories
# ============================================================

from __future__ import annotations

import math
import re
from typing import Dict, List, Literal, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

from careers.profiles import CATEGORIES
from careers.recommender import get_career_detail, recommend_careers

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

router = APIRouter(prefix="/api/v1/careers", tags=["careers"])

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OCEAN_TRAITS: frozenset[str] = frozenset(
    {
        "Openness",
        "Conscientiousness",
        "Extraversion",
        "Agreeableness",
        "Neuroticism",
    }
)

CAREER_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")

TOP_N_MIN = 1
TOP_N_MAX = 50
TOP_N_DEFAULT = 10

FIT_SCORE_MIN = 0.0
FIT_SCORE_MAX = 100.0
FIT_SCORE_DEFAULT = 60.0

ValidUserType = Literal[
    "class_10",
    "class_12",
    "undergraduate",
    "professional",
]

ValidSourceFilter = Literal[
    "onet",
    "indian",
    "hybrid",
]

# ---------------------------------------------------------------------------
# OCEAN validator
# ---------------------------------------------------------------------------


def validate_ocean(scores: Dict[str, float]) -> Dict[str, float]:
    """
    Validates:
    - exactly 5 OCEAN keys
    - numeric finite values only
    - values within [0, 100]
    """

    if not isinstance(scores, dict):
        raise ValueError("ocean_scores must be a JSON object.")

    provided = set(scores.keys())

    missing = OCEAN_TRAITS - provided
    if missing:
        raise ValueError(
            f"Missing OCEAN trait(s): {sorted(missing)}"
        )

    extra = provided - OCEAN_TRAITS
    if extra:
        raise ValueError(
            f"Unexpected key(s): {sorted(extra)}"
        )

    for trait, value in scores.items():

        # Reject booleans explicitly
        if isinstance(value, bool):
            raise ValueError(
                f"'{trait}' must be numeric, not boolean."
            )

        if not isinstance(value, (int, float)):
            raise ValueError(
                f"'{trait}' must be numeric."
            )

        if math.isnan(value) or math.isinf(value):
            raise ValueError(
                f"'{trait}' must be finite."
            )

        if not (FIT_SCORE_MIN <= value <= FIT_SCORE_MAX):
            raise ValueError(
                f"'{trait}' value {value} is outside [0, 100]."
            )

    return scores


# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------


class RecommendRequest(BaseModel):

    ocean_scores: Dict[str, float] = Field(
        ...,
        description="Exactly five OCEAN scores in [0, 100].",
    )

    user_type: ValidUserType

    top_n: int = Field(
        default=TOP_N_DEFAULT,
        ge=TOP_N_MIN,
        le=TOP_N_MAX,
    )

    category_filter: Optional[str] = None

    source_filter: Optional[ValidSourceFilter] = None

    min_fit_score: float = Field(
        default=FIT_SCORE_DEFAULT,
        ge=FIT_SCORE_MIN,
        le=FIT_SCORE_MAX,
    )

    @field_validator("ocean_scores")
    @classmethod
    def check_ocean(
        cls,
        value: Dict[str, float]
    ) -> Dict[str, float]:
        return validate_ocean(value)

    @model_validator(mode="after")
    def check_category_filter(self):

        if (
            self.category_filter is not None
            and self.category_filter not in CATEGORIES
        ):
            raise ValueError(
                f"'{self.category_filter}' is not a valid category."
            )

        return self


class CareerDetailRequest(BaseModel):

    ocean_scores: Dict[str, float]

    @field_validator("ocean_scores")
    @classmethod
    def check_ocean(
        cls,
        value: Dict[str, float]
    ) -> Dict[str, float]:
        return validate_ocean(value)


# ---------------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------------


class CareerSummary(BaseModel):

    career_id: str
    title: str
    category: str
    fit_score: float
    source: Optional[str] = None


class ResponseMetadata(BaseModel):

    filters_applied: Dict[str, object]

    scoring_method: str

    warnings: List[str] = Field(default_factory=list)


class RecommendResponse(BaseModel):

    user_type: str

    total_returned: int

    careers: List[CareerSummary]

    metadata: ResponseMetadata


class TraitGap(BaseModel):

    trait: str
    user_score: float
    required_score: float
    gap: float


class CareerDetailResponse(BaseModel):

    career_id: str

    title: str

    category: str

    fit_score: float

    trait_gaps: List[TraitGap] = Field(default_factory=list)


class CategoriesResponse(BaseModel):

    categories: List[str]


# ---------------------------------------------------------------------------
# Mapping Layer
# ---------------------------------------------------------------------------


def _map_career_summary(raw: Dict) -> CareerSummary:

    try:
        return CareerSummary(
            career_id=raw["id"],
            title=raw["name"],
            category=raw["category"],
            fit_score=raw["score"],
            source=raw.get("source"),
        )

    except KeyError as exc:
        raise ValueError(
            f"Invalid recommender career shape. Missing key: {exc}"
        ) from exc


def _map_trait_gap(raw: Dict) -> TraitGap:

    try:
        return TraitGap(
            trait=raw["trait"],
            user_score=raw["user"],
            required_score=raw["required"],
            gap=raw["gap"],
        )

    except KeyError as exc:
        raise ValueError(
            f"Invalid recommender gap shape. Missing key: {exc}"
        ) from exc


def _map_career_detail(raw: Dict) -> CareerDetailResponse:

    try:
        return CareerDetailResponse(
            career_id=raw["id"],
            title=raw["name"],
            category=raw["category"],
            fit_score=raw["score"],
            trait_gaps=[
                _map_trait_gap(g)
                for g in raw.get("gaps", [])
            ],
        )

    except KeyError as exc:
        raise ValueError(
            f"Invalid recommender detail shape. Missing key: {exc}"
        ) from exc


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------


def _validate_career_id(career_id: str) -> None:

    if not CAREER_ID_PATTERN.match(career_id):

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid career_id format. "
                "Allowed: alphanumeric, hyphen, underscore."
            ),
        )


def _build_metadata(
    req: RecommendRequest,
    warnings: List[str],
) -> ResponseMetadata:

    return ResponseMetadata(
        filters_applied={
            "category_filter": req.category_filter,
            "source_filter": req.source_filter,
            "min_fit_score": req.min_fit_score,
            "top_n": req.top_n,
        },
        scoring_method="ocean_weighted_fit",
        warnings=warnings,
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post(
    "/recommend",
    response_model=RecommendResponse,
    summary="Get personalised career recommendations",
)
def get_recommendations(
    req: RecommendRequest
) -> RecommendResponse:

    try:

        raw = recommend_careers(
            ocean_scores=req.ocean_scores,
            user_type=req.user_type,
            top_n=req.top_n,
            category_filter=req.category_filter,
            source_filter=req.source_filter,
            min_fit_score=req.min_fit_score,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except LookupError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail="Recommendation engine error.",
        ) from exc

    try:

        careers = [
            _map_career_summary(c)
            for c in raw.get("careers", [])
        ]

    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    warnings: List[str] = []

    if req.min_fit_score > 80:
        warnings.append(
            "Very high min_fit_score may reduce results."
        )

    return RecommendResponse(
        user_type=req.user_type,
        total_returned=len(careers),
        careers=careers,
        metadata=_build_metadata(req, warnings),
    )


@router.post(
    "/{career_id}",
    response_model=CareerDetailResponse,
    summary="Get detailed career analysis",
)
def career_detail(
    career_id: str,
    req: CareerDetailRequest,
) -> CareerDetailResponse:

    _validate_career_id(career_id)

    try:

        raw = get_career_detail(
            career_id,
            req.ocean_scores,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except LookupError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail="Career detail lookup failed.",
        ) from exc

    if isinstance(raw, dict) and "error" in raw:

        raise HTTPException(
            status_code=404,
            detail=raw["error"],
        )

    try:

        return _map_career_detail(raw)

    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc


@router.get(
    "/categories",
    response_model=CategoriesResponse,
    summary="List available career categories",
)
def list_categories() -> CategoriesResponse:

    try:

        clean = sorted(
            str(c)
            for c in CATEGORIES
            if c is not None
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail="Could not load categories.",
        ) from exc

    return CategoriesResponse(
        categories=clean
    )

