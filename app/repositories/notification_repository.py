from email.policy import default

from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.notification import Notification
from app.repositories.user_repository import get_by_email
from fastapi import HTTPException

def create_notification(
    db: Session,
    title: str,
    message: str,
    channel: str,
    email: str,
    user_id: int,

):
    recipient = get_by_email(db, email=email)
    if recipient is None:
        raise HTTPException(status_code=404, detail="Recipient not found")

    notification = Notification(
        title=title,
        message=message,
        channel=channel,
        sent_by=user_id,
        recipient_id=recipient.id
    )

    db.add(notification)

    db.commit()

    db.refresh(notification)

    return notification

def get_notifications_by_user(
    db: Session,
    user_id: int
):

    return (
        db.query(Notification)
        .filter(or_(Notification.recipient_id == user_id,
                    Notification.sent_by == user_id))
        .order_by(Notification.created_at.desc())
        .all()
    )

def mark_as_sent(
    db: Session,
    user_id: int
):
    db.query(Notification).filter(
        Notification.recipient_id == user_id,
        Notification.status == "PENDING"
    ).update(
        {"status": "SENT"}
    )

    db.commit()

def get_notifications(
    db: Session,
    user_id: int,
    status: str = None,
    channel: str = None,
    title: str = None,
    sent_by: str = None,
):
    query = db.query(Notification).filter(or_(Notification.recipient_id == user_id,
                    Notification.sent_by == user_id))

    if status:
        query = query.filter(
            Notification.status == status
        )

    if channel:
        query = query.filter(
            Notification.channel == channel
        )

    if title:
        query = query.filter(
            Notification.title.ilike(f"%{title}%")
        )

    if sent_by:
        query = query.filter(
            Notification.sent_by == int(sent_by)
        )

    return query.order_by(
        Notification.created_at.desc()
    ).all()

def get_notification_by_id(
    db: Session,
    notification_id: int,
    user_id: int
):
    return (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.recipient_id == user_id
        )
        .first()
    )

def update_notification_status(
    db: Session,
    notification_id: int,
    user_id: int,
    status: str
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.recipient_id == user_id
        )
        .first()
    )

    if notification:
        notification.status = status
        db.commit()
        db.refresh(notification)

    return notification

def delete_notification(
    db: Session,
    notification_id: int,
    user_id: int
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.recipient_id == user_id
        )
        .first()
    )

    if notification is None:
        return None

    db.delete(notification)

    db.commit()

    return True

