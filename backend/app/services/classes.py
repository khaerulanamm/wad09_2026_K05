from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from app.models.gym_class import GymClass


def get_class_or_404(db: DbSession, class_id: int) -> GymClass:
    item = db.get(GymClass, class_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Kelas tidak ditemukan.")
    return item


def has_schedule_conflict(
    db: DbSession, instructor: str, class_date, start_time, exclude_id: int | None = None
) -> bool:
    query = select(GymClass.id).where(
        GymClass.instructor == instructor,
        GymClass.date == class_date,
        GymClass.start_time == start_time,
    )
    if exclude_id is not None:
        query = query.where(GymClass.id != exclude_id)
    return db.scalar(query.limit(1)) is not None
