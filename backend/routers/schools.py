# routers/schools.py
from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException, status
from db.client import get_supabase
from schemas.schemas import SchoolCreate, SchoolRead

logger = logging.getLogger("edwiserr.schools")
router = APIRouter(tags=["Schools"])


@router.post("/schools", response_model=SchoolRead, status_code=status.HTTP_201_CREATED)
def create_school(payload: SchoolCreate) -> SchoolRead:
    sb  = get_supabase()
    res = sb.table("schools").insert(payload.model_dump(exclude_none=True)).execute()

    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create school.")

    logger.info("School created: %s", res.data[0].get("id"))
    return SchoolRead(**res.data[0])


@router.get("/schools", response_model=list[SchoolRead])
def list_schools(skip: int = 0, limit: int = 100) -> list[SchoolRead]:
    sb  = get_supabase()
    res = sb.table("schools").select("*").range(skip, skip + limit - 1).execute()
    return [SchoolRead(**r) for r in res.data]


@router.get("/schools/{school_id}", response_model=SchoolRead)
def get_school(school_id: int) -> SchoolRead:
    sb  = get_supabase()
    res = sb.table("schools").select("*").eq("id", school_id).maybe_single().execute()

    if not res.data:
        raise HTTPException(status_code=404, detail=f"School id={school_id} not found.")

    return SchoolRead(**res.data)