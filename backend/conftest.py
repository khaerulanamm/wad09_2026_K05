import os
import sys

# Pastikan folder `backend/` (lokasi file ini) ada di sys.path agar package
# `app` dapat diimpor saat pytest dijalankan dari mana pun. conftest berada di
# root backend/ supaya fixture dipakai bersama oleh tests/ dan app/test/.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("JWT_SECRET", "test-only-secret-for-pytest-long-enough-32-bytes")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.security import hash_password
from app.models.user import User


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _record):
        connection.execute("PRAGMA foreign_keys=ON")

    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.state.test_session_factory = TestingSession
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)
    engine.dispose()


def register(client: TestClient, name="Trainer", email="trainer@example.com"):
    create_admin(client)
    response = client.post(
        "/auth/register",
        json={"name": name, "email": email, "password": "password123"},
        headers=login(client, "admin@example.com"),
    )
    assert response.status_code == 201, response.text
    return response.json()


def login(client: TestClient, email="trainer@example.com"):
    response = client.post("/auth/login", json={"email": email, "password": "password123"})
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def create_admin(client: TestClient):
    with client.app.state.test_session_factory() as db:
        existing = db.scalar(select(User).where(User.email == "admin@example.com"))
        if existing:
            return existing.id
        user = User(
            name="Admin",
            email="admin@example.com",
            password_hash=hash_password("password123"),
            role="admin",
        )
        db.add(user)
        db.commit()
        return user.id

