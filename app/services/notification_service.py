from app.repositories.notification_repository import (
    create_notification, get_notifications, get_notifications_by_user, get_notification_by_id, delete_notification, update_notification_status
)
from fastapi import HTTPException


def create(db, data, current_user):
    return create_notification(
        db,
        data.title,
        data.message,

        data.channel,
        data.recipient,
        current_user.id,
    )

def get_all(
    db,
    current_user,
    status=None,
    channel=None,
    title=None,
    sent_by=None,
):
    notifications = get_notifications(
        db,
        current_user.id,
        status,
        channel,
        title,
        sent_by
    )

    return notifications

def get_all_by_user(
    db,
    current_user
):
    return get_notifications_by_user(db, current_user.id)

def get_by_id(db,
              id,
              current_user):
    notification = get_notification_by_id(db, id,current_user.id)

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found")

    return get_notification_by_id(db, id, current_user.id)

def update_status(
    db,
    notification_id,
    data,
    current_user
):
    notification = update_notification_status(
        db,
        notification_id,
        current_user.id,
        data.status
    )

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return notification

def delete(
    db,
    notification_id,
    current_user
):
    result = delete_notification(
        db,
        notification_id,
        current_user.id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return {
        "message": "Notification deleted successfully"
    }