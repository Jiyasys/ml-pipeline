# ============================================================
# EDWISERR — Careers Router (FastAPI)
# POST /api/careers/recommend  → top career matches
# GET  /api/careers/{id}       → single career detail
# GET  /api/careers/categories → available categories
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

from careers.recommender import recommend_careers, get_career_detail
from careers.profiles    import CATEGORIES

router = APIRouter()

class RecommendRequest(BaseModel):
    ocean_scores:    Dict[str, float]   # {trait: 0-100}
    user_type:       str
    top_n:           Optional[int]   = 10
    category_filter: Optional[str]  = None
    source_filter:   Optional[str]  = None   # 'onet' | 'indian' | 'hybrid'
    min_fit_score:   Optional[float] = 60.0

class CareerDetailRequest(BaseModel):
    ocean_scores: Dict[str, float]

@router.post('/recommend')
def get_recommendations(req: RecommendRequest):
    """
    Main recommendation endpoint.
    Send OCEAN scores from the personality engine output.
    """
    result = recommend_careers(
        ocean_scores    = req.ocean_scores,
        user_type       = req.user_type,
        top_n           = req.top_n,
        category_filter = req.category_filter,
        source_filter   = req.source_filter,
        min_fit_score   = req.min_fit_score,
    )
    return result

@router.post('/{career_id}')
def career_detail(career_id: str, req: CareerDetailRequest):
    """Full detail for a single career with trait gap breakdown."""
    result = get_career_detail(career_id, req.ocean_scores)
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    return result

@router.get('/categories')
def list_categories():
    """All available career categories."""
    return {'categories': CATEGORIES}