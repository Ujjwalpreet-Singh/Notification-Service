from fastapi import HTTPException

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.repositories.user_repository import (
    get_by_email,
    create_user
)

from app.repositories.notification_repository import (
    mark_as_sent
)


def register(db, data):
    existing_user = get_by_email(
        db,
        data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed = hash_password(data.password)

    return create_user(
        db,
        data.username,
        hashed,
        data.email
    )


def login(db, data):
    user = get_by_email(
        db,
        data.email
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {"sub": str(user.id)}
    )
    mark_as_sent(db,user.id)
    return {
        "access_token": token,
        "token_type": "bearer"
    }