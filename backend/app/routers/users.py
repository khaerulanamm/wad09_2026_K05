from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserOut, UserUpdateIn
from app.security import ensure_owner_or_admin, get_current_user


router = APIRouter(prefix="/users", tags=["users"])


def get_user_or_404(user_id: int, db: Session) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User tidak ditemukan.")
    return user


@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    user = get_user_or_404(user_id, db)
    ensure_owner_or_admin(user.id, current)
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: UserUpdateIn,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    user = get_user_or_404(user_id, db)
    ensure_owner_or_admin(user.id, current)
    changes = payload.model_dump(exclude_unset=True, exclude_none=True)
    if "email" in changes and changes["email"] != user.email:
        if db.scalar(select(User).where(User.email == changes["email"])):
            raise HTTPException(status_code=409, detail="Email sudah terdaftar.")
    for field, value in changes.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user
