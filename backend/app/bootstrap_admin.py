"""Create the first admin from operator-provided environment variables."""

import os

from sqlalchemy import select

from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password


def main() -> None:
    email = os.environ["BOOTSTRAP_ADMIN_EMAIL"].strip().lower()
    password = os.environ["BOOTSTRAP_ADMIN_PASSWORD"]
    name = os.getenv("BOOTSTRAP_ADMIN_NAME", "UAS Demo Admin").strip()
    if not email or len(password) < 8 or len(password.encode("utf-8")) > 72 or not name:
        raise ValueError("Email, nama, dan password admin (8–72 byte) wajib diisi.")

    with SessionLocal() as db:
        existing = db.scalar(select(User).where(User.email == email))
        if existing:
            if existing.role != "admin":
                raise ValueError("Email sudah dipakai akun non-admin.")
            print("Admin sudah tersedia.")
            return
        db.add(User(name=name, email=email, password_hash=hash_password(password), role="admin"))
        db.commit()
        print("Admin berhasil dibuat.")


if __name__ == "__main__":
    main()
