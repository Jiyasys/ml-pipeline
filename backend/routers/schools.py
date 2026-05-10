"""
routers/schools.py
------------------
School registration and lookup endpoints.
"""

from __future__ import annotations

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud.crud import create_school, get_school, list_schools
from db.deps import get_db
from models.models import School
from schemas.schemas import SchoolCreate, SchoolRead

router = APIRouter(
    prefix="/api/v1/schools",
    tags=["Schools"],
)


@router.post(
    "",
    response_model=SchoolRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new school",
)
def register_school(
    payload: SchoolCreate,
    db: Session = Depends(get_db),
) -> School:
    return create_school(db, payload)


@router.get(
    "",
    response_model=list[SchoolRead],
    summary="List all schools",
)
def get_schools(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Sequence[School]:
    return list_schools(db, skip=skip, limit=limit)


@router.get(
    "/{school_id}",
    response_model=SchoolRead,
    summary="Get a school by ID",
)
def get_school_by_id(
    school_id: int,
    db: Session = Depends(get_db),
) -> School:
    school = get_school(db, school_id)
    if school is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"School id={school_id} not found.",
        )
    return school