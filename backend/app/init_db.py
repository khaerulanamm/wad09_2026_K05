"""Create the two project tables with SQLAlchemy on first setup."""

from sqlalchemy import inspect

from app.database import Base, engine
from app.models import GymClass, User  # noqa: F401 - register tables with Base


def main() -> None:
    tables = set(inspect(engine).get_table_names())
    if "sessions" in tables:
        if "classes" in tables:
            raise RuntimeError("Tabel sessions dan classes sama-sama ada; periksa database sebelum setup.")
        with engine.begin() as connection:
            connection.exec_driver_sql("ALTER TABLE sessions RENAME TO classes")
    Base.metadata.create_all(bind=engine)
    print("Tabel users dan classes siap.")


if __name__ == "__main__":
    main()
