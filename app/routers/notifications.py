from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import (
    get_db,
    get_current_user
)
from app.models.user import User
from app.schemas.notifications import (
    NotificationCreate,NotificationUpdate
)
from app.services.notification_service import create, get_all, get_all_by_user, get_by_id,update_status,delete

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.post("/create")
def create_notification(
    data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create(
        db,
        data,
        current_user
    )

@router.get("/all")
def get_notifications_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_by_user(
        db,
        current_user
    )

@router.get("/")
def get_notifications(
    status: str = None,
    channel: str = None,
    title: str = None,
    sent_by: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all(
        db,
        current_user,
        status,
        channel,
        title,
        sent_by
    )

@router.get("/{notification_id}")
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_by_id(
        db,
        notification_id,
        current_user
    )

@router.patch("/{notification_id}")
def patch_notification(
    notification_id: int,
    data: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_status(
        db,
        notification_id,
        data,
        current_user
    )

@router.delete("/{notification_id}")
def delete_notification(
        notification_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return delete(db, notification_id, current_user)