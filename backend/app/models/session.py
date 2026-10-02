import datetime as dt
from typing import Literal
from pydantic import BaseModel, Field

Level = Literal["beginner", "intermediate", "advanced"]

class SessionIn(BaseModel):
    class_name: str = Field(..., min_length=1)
    instructor: str = Field(..., min_length=1)
    date: dt.date
    start_time: str
    duration_min: int = Field(..., ge=15, le=180)
    capacity: int = Field(..., ge=1, le=50)
    level: Level

class SessionOut(SessionIn):
    id: int
