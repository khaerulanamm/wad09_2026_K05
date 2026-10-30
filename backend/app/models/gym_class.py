from datetime import date as DateValue, datetime, time as TimeValue

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class GymClass(Base):
    __tablename__ = "classes"
    __table_args__ = (
        CheckConstraint("level IN ('beginner', 'intermediate', 'advanced')", name="ck_classes_level"),
        CheckConstraint("duration_min BETWEEN 15 AND 180", name="ck_classes_duration"),
        CheckConstraint("capacity BETWEEN 1 AND 50", name="ck_classes_capacity"),
        Index("ix_classes_owner_date", "owner_id", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    class_name: Mapped[str] = mapped_column(String(60), nullable=False)
    instructor: Mapped[str] = mapped_column(String(60), nullable=False)
    date: Mapped[DateValue] = mapped_column(nullable=False)
    start_time: Mapped[TimeValue] = mapped_column(Time, nullable=False)
    duration_min: Mapped[int] = mapped_column(nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)
    level: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    owner: Mapped["User"] = relationship(back_populates="classes")
