import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from app.repositories.notification_repository import (
create_notification,
update_notification_status,
delete_notification
)

def test_create_notification_success():
    db = Mock()


    recipient = Mock()
    recipient.id = 2

    with patch(
        "app.repositories.notification_repository.get_by_email",
        return_value=recipient
    ):

        notification = create_notification(
            db=db,
            title="Welcome",
            message="Hello",
            channel="EMAIL",
            email="recipient@test.com",
            user_id=1
        )

        assert notification.title == "Welcome"
        assert notification.message == "Hello"
        assert notification.channel == "EMAIL"
        assert notification.sent_by == 1
        assert notification.recipient_id == 2

        db.add.assert_called_once()
        db.commit.assert_called_once()
        db.refresh.assert_called_once()


def test_create_notification_recipient_not_found():
    db = Mock()


    with patch(
        "app.repositories.notification_repository.get_by_email",
        return_value=None
    ):

        with pytest.raises(HTTPException) as exc:
            create_notification(
                db=db,
                title="Welcome",
                message="Hello",
                channel="EMAIL",
                email="missing@test.com",
                user_id=1
            )

        assert exc.value.status_code == 404
        assert exc.value.detail == "Recipient not found"

        db.add.assert_not_called()
        db.commit.assert_not_called()


def test_update_notification_status_success():
    db = Mock()


    notification = Mock()
    notification.status = "PENDING"

    query = Mock()
    query.filter.return_value.first.return_value = notification

    db.query.return_value = query

    result = update_notification_status(
        db=db,
        notification_id=1,
        user_id=2,
        status="SENT"
    )

    assert result == notification
    assert notification.status == "SENT"

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(notification)


def test_update_notification_status_not_found():
    db = Mock()


    query = Mock()
    query.filter.return_value.first.return_value = None

    db.query.return_value = query

    result = update_notification_status(
        db=db,
        notification_id=999,
        user_id=2,
        status="SENT"
    )

    assert result is None

    db.commit.assert_not_called()

def test_delete_notification_success():
    db = Mock()


    notification = Mock()

    query = Mock()
    query.filter.return_value.first.return_value = notification

    db.query.return_value = query

    result = delete_notification(
        db=db,
        notification_id=1,
        user_id=2
    )

    assert result is True

    db.delete.assert_called_once_with(notification)
    db.commit.assert_called_once()


def test_delete_notification_not_found():
    db = Mock()


    query = Mock()
    query.filter.return_value.first.return_value = None

    db.query.return_value = query

    result = delete_notification(
        db=db,
        notification_id=999,
        user_id=2
    )

    assert result is None

    db.delete.assert_not_called()
    db.commit.assert_not_called()

