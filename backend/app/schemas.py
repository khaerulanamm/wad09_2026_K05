"""B3: skema masuk dan keluar dipisah.

SessionIn adalah apa yang boleh dikirim klien (tanpa id, karena id dibuat server).
SessionOut adalah apa yang dikembalikan server (dengan id).
"""

import datetime as dt
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Level = Literal["beginner", "intermediate", "advanced"]


class SessionIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    class_name: str = Field(min_length=1, max_length=60, examples=["Yoga Pagi"])
    instructor: str = Field(min_length=1, max_length=60, examples=["Rina Saputri"])
    date: dt.date = Field(examples=["2026-10-05"])
    start_time: str = Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$", examples=["07:00"])
    duration_min: int = Field(ge=15, le=180, examples=[60])
    capacity: int = Field(ge=1, le=50, examples=[20])
    level: Level


class SessionOut(SessionIn):
    id: int
