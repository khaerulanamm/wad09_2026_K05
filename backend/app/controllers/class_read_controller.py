from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session as DbSession

from app.database import get_db
from app.models.gym_class import GymClass
from app.schemas.classes import ClassOut, ClassPage
from app.services.classes import get_class_or_404


router = APIRouter(prefix="/classes", tags=["classes"])


@router.get("", response_model=ClassPage)
def list_classes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    search: str = Query("", max_length=50),
    db: DbSession = Depends(get_db),
):
    query = select(GymClass)
    count_query = select(func.count(GymClass.id))
    keyword = search.strip()
    if keyword:
        condition = or_(GymClass.class_name.ilike(f"%{keyword}%"), GymClass.instructor.ilike(f"%{keyword}%"))
        query = query.where(condition)
        count_query = count_query.where(condition)
    items = db.scalars(query.order_by(GymClass.date, GymClass.start_time, GymClass.id).offset(skip).limit(limit)).all()
    return {"items": items, "total": db.scalar(count_query) or 0, "skip": skip, "limit": limit}


@router.get("/{class_id}", response_model=ClassOut)
def get_class(class_id: int, db: DbSession = Depends(get_db)):
    return get_class_or_404(db, class_id)
