from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.auth import (
    UserCreate,
    UserLogin
)
from app.services.auth_service import (
    register,
    login
)
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    user = register(
        db,
        data
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }


@router.post("/login")
def login_user(
    data: UserLogin,
    db: Session = Depends(get_db)
):

    return login(
        db,
        data
    )

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }