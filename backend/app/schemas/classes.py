from datetime import date as DateValue, time as TimeValue

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.common import Level


class ClassCreate(BaseModel):
    class_name: str = Field(min_length=1, max_length=60)
    instructor: str = Field(min_length=1, max_length=60)
    date: DateValue
    start_time: TimeValue
    duration_min: int = Field(ge=15, le=180)
    capacity: int = Field(ge=1, le=50)
    level: Level

    @field_validator("class_name", "instructor")
    @classmethod
    def trim_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Kolom ini wajib diisi.")
        return value


class ClassUpdate(BaseModel):
    class_name: str | None = Field(default=None, min_length=1, max_length=60)
    instructor: str | None = Field(default=None, min_length=1, max_length=60)
    date: DateValue | None = None
    start_time: TimeValue | None = None
    duration_min: int | None = Field(default=None, ge=15, le=180)
    capacity: int | None = Field(default=None, ge=1, le=50)
    level: Level | None = None

    @field_validator("class_name", "instructor")
    @classmethod
    def trim_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("Kolom ini wajib diisi.")
        return value


class ClassOut(BaseModel):
    id: int
    owner_id: int
    class_name: str
    instructor: str
    date: DateValue
    start_time: TimeValue
    duration_min: int
    capacity: int
    level: Level

    model_config = ConfigDict(from_attributes=True)


class ClassPage(BaseModel):
    items: list[ClassOut]
    total: int
    skip: int
    limit: int
