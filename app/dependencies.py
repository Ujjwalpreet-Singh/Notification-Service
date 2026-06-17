from jose import jwt

from app.core.database import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.repositories.user_repository import get_by_id


security = HTTPBearer()

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )

    user = get_by_id(db, int(user_id))

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )

    return user
