import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import schemas
from school.crud import crud
from database import get_db

router = APIRouter(prefix="/score", tags=["Student Top Score CRUD"])


@router.post("/topscore/", response_model=List[schemas.TopperStudentOut])
def store_top_score(
    min_score: int = Query(..., gt=70, le=100), db: Session = Depends(get_db)
):
    """
    Store students with score >= min_score into the TopperStudent table,
    then return those entries along with school_name.
    """
    crud.insert_top_score(db, min_score)
    toppers = crud.get_toppers_with_school_name(db)
    return toppers
