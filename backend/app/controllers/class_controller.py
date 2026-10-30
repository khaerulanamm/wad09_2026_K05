from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session as DbSession

from app.database import get_db
from app.models.gym_class import GymClass
from app.models.user import User
from app.schemas.classes import ClassCreate, ClassOut, ClassUpdate
from app.security import ensure_owner_or_admin, get_current_user
from app.services.classes import get_class_or_404, has_schedule_conflict


router = APIRouter(prefix="/classes", tags=["classes"])


@router.post("", response_model=ClassOut, status_code=status.HTTP_201_CREATED)
def create_class(
    payload: ClassCreate,
    db: DbSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if has_schedule_conflict(db, payload.instructor, payload.date, payload.start_time):
        raise HTTPException(status_code=409, detail="Instruktur sudah memiliki kelas pada waktu tersebut.")
    item = GymClass(owner_id=user.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{class_id}", response_model=ClassOut)
def update_class(
    class_id: int,
    payload: ClassUpdate,
    db: DbSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = get_class_or_404(db, class_id)
    ensure_owner_or_admin(item.owner_id, user)
    changes = payload.model_dump(exclude_unset=True, exclude_none=True)
    instructor = changes.get("instructor", item.instructor)
    class_date = changes.get("date", item.date)
    start_time = changes.get("start_time", item.start_time)
    if has_schedule_conflict(db, instructor, class_date, start_time, exclude_id=item.id):
        raise HTTPException(status_code=409, detail="Instruktur sudah memiliki kelas pada waktu tersebut.")
    for field, value in changes.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(
    class_id: int,
    db: DbSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = get_class_or_404(db, class_id)
    ensure_owner_or_admin(item.owner_id, user)
    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
