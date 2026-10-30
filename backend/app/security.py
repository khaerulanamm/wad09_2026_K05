import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User


bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(user: User) -> str:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET belum dikonfigurasi.")
    expires = datetime.now(timezone.utc) + timedelta(minutes=45)
    payload = {"sub": str(user.id), "role": user.role, "exp": expires}
    return jwt.encode(payload, secret, algorithm="HS256")


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Autentikasi diperlukan.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    secret = os.getenv("JWT_SECRET")
    if credentials is None or not secret:
        raise unauthorized
    try:
        payload = jwt.decode(credentials.credentials, secret, algorithms=["HS256"])
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
        raise unauthorized
    user = db.get(User, user_id)
    if user is None:
        raise unauthorized
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Akses admin diperlukan.")
    return user


def ensure_owner_or_admin(owner_id: int, user: User) -> None:
    if user.role != "admin" and user.id != owner_id:
        raise HTTPException(status_code=403, detail="Kamu tidak memiliki akses ke resource ini.")
