import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from app.services.notification_service import (
    create,
    get_all,
    get_all_by_user,
    get_by_id,
    update_status,
    delete
)


def test_create_notification():
    db = Mock()

    current_user = Mock()
    current_user.id = 1

    data = Mock()
    data.title = "Welcome"
    data.message = "Hello"
    data.channel = "EMAIL"
    data.recipient = "recipient@test.com"

    expected_notification = Mock()

    with patch(
        "app.services.notification_service.create_notification",
        return_value=expected_notification
    ) as mock_create:

        result = create(
            db,
            data,
            current_user
        )

        assert result == expected_notification

        mock_create.assert_called_once_with(
            db,
            "Welcome",
            "Hello",
            "EMAIL",
            "recipient@test.com",
            1
        )


def test_get_all_notifications():
    db = Mock()

    current_user = Mock()
    current_user.id = 1

    expected_notifications = [
        Mock(),
        Mock()
    ]

    with patch(
        "app.services.notification_service.get_notifications",
        return_value=expected_notifications
    ) as mock_get:

        result = get_all(
            db,
            current_user
        )

        assert result == expected_notifications

        mock_get.assert_called_once_with(
            db,
            1,
            None,
            None,
            None,
            None
        )


def test_get_all_notifications_with_filters():
    db = Mock()

    current_user = Mock()
    current_user.id = 1

    with patch(
        "app.services.notification_service.get_notifications",
        return_value=[]
    ) as mock_get:

        get_all(
            db,
            current_user,
            status="SENT",
            channel="EMAIL",
            title="Welcome",
            sent_by="2"
        )

        mock_get.assert_called_once_with(
            db,
            1,
            "SENT",
            "EMAIL",
            "Welcome",
            "2"
        )


def test_get_all_by_user():
    db = Mock()

    current_user = Mock()
    current_user.id = 1

    expected_notifications = [Mock()]

    with patch(
        "app.services.notification_service.get_notifications_by_user",
        return_value=expected_notifications
    ) as mock_get:

        result = get_all_by_user(
            db,
            current_user
        )

        assert result == expected_notifications

        mock_get.assert_called_once_with(
            db,
            1
        )


def test_get_notification_by_id_success():
    db = Mock()

    current_user = Mock()
    current_user.id = 1

    notification = Mock()

    with patch(
        "app.services.notification_service.get_notification_by_id",
        return_value=notification
    ):

        result = get_by_id(
            db,
            1,
            current_user
        )

        assert result == notification


def test_get_notification_by_id_not_found():
    db = Mock()

    current_user = Mock()
    current_user.id = 1

    with patch(
        "app.services.notification_service.get_notification_by_id",
        return_value=None
    ):

        with pytest.raises(HTTPException) as exc:
            get_by_id(
                db,
                999,
                current_user
            )

        assert exc.value.status_code == 404
        assert exc.value.detail == "Notification not found"


def test_update_notification_status_success():
    db = Mock()

    current_user = Mock()
    current_user.id = 1

    data = Mock()
    data.status = "SENT"

    updated_notification = Mock()

    with patch(
        "app.services.notification_service.update_notification_status",
        return_value=updated_notification
    ) as mock_update:

        result = update_status(
            db,
            1,
            data,
            current_user
        )

        assert result == updated_notification

        mock_update.assert_called_once_with(
            db,
            1,
            1,
            "SENT"
        )


def test_update_notification_status_not_found():
    db = Mock()

    current_user = Mock()
    current_user.id = 1

    data = Mock()
    data.status = "SENT"

    with patch(
        "app.services.notification_service.update_notification_status",
        return_value=None
    ):

        with pytest.raises(HTTPException) as exc:
            update_status(
                db,
                999,
                data,
                current_user
            )

        assert exc.value.status_code == 404
        assert exc.value.detail == "Notification not found"


def test_delete_notification_success():
    db = Mock()

    current_user = Mock()
    current_user.id = 1

    with patch(
        "app.services.notification_service.delete_notification",
        return_value=True
    ):

        result = delete(
            db,
            1,
            current_user
        )

        assert result == {
            "message": "Notification deleted successfully"
        }


def test_delete_notification_not_found():
    db = Mock()

    current_user = Mock()
    current_user.id = 1

    with patch(
        "app.services.notification_service.delete_notification",
        return_value=None
    ):

        with pytest.raises(HTTPException) as exc:
            delete(
                db,
                999,
                current_user
            )

        assert exc.value.status_code == 404
        assert exc.value.detail == "Notification not found"