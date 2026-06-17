from sqlalchemy.orm import Session

from app.models.user import User


def get_by_email(
    db: Session,
    email: str
):

    return db.query(User).filter(
        User.email == email
    ).first()

def get_by_id(
    db: Session,
    user_id: int
):
    return db.query(User).filter(
        User.id == user_id
    ).first()

def create_user(
    db: Session,
    username: str,
    password_hash: str,
    email: str
):
    user = User(
        username=username,
        password_hash=password_hash,
        email=email

    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user