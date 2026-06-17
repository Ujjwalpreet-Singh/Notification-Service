import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from app.services.auth_service import (
    register,
    login
)


def test_register_success():
    db = Mock()

    data = Mock()
    data.username = "john"
    data.email = "john@example.com"
    data.password = "password123"

    created_user = Mock()

    with patch(
        "app.services.auth_service.get_by_email",
        return_value=None
    ):
        with patch(
            "app.services.auth_service.hash_password",
            return_value="hashed_password"
        ) as mock_hash:
            with patch(
                "app.services.auth_service.create_user",
                return_value=created_user
            ) as mock_create:

                result = register(
                    db,
                    data
                )

                assert result == created_user

                mock_hash.assert_called_once_with(
                    "password123"
                )

                mock_create.assert_called_once_with(
                    db,
                    "john",
                    "hashed_password",
                    "john@example.com"
                )


def test_register_duplicate_email():
    db = Mock()

    data = Mock()
    data.email = "john@example.com"

    with patch(
        "app.services.auth_service.get_by_email",
        return_value=Mock()
    ):

        with pytest.raises(HTTPException) as exc:
            register(
                db,
                data
            )

        assert exc.value.status_code == 400
        assert exc.value.detail == "Email already registered"


def test_login_user_not_found():
    db = Mock()

    data = Mock()
    data.email = "missing@example.com"
    data.password = "password123"

    with patch(
        "app.services.auth_service.get_by_email",
        return_value=None
    ):

        with pytest.raises(HTTPException) as exc:
            login(
                db,
                data
            )

        assert exc.value.status_code == 401
        assert exc.value.detail == "Invalid credentials"


def test_login_invalid_password():
    db = Mock()

    user = Mock()
    user.password_hash = "hashed"

    data = Mock()
    data.email = "john@example.com"
    data.password = "wrongpassword"

    with patch(
        "app.services.auth_service.get_by_email",
        return_value=user
    ):
        with patch(
            "app.services.auth_service.verify_password",
            return_value=False
        ):

            with pytest.raises(HTTPException) as exc:
                login(
                    db,
                    data
                )

            assert exc.value.status_code == 401
            assert exc.value.detail == "Invalid credentials"


def test_login_success():
    db = Mock()

    user = Mock()
    user.id = 1
    user.password_hash = "hashed_password"

    data = Mock()
    data.email = "john@example.com"
    data.password = "password123"

    with patch(
        "app.services.auth_service.get_by_email",
        return_value=user
    ):
        with patch(
            "app.services.auth_service.verify_password",
            return_value=True
        ) as mock_verify:
            with patch(
                "app.services.auth_service.create_access_token",
                return_value="jwt-token"
            ) as mock_token:
                with patch(
                    "app.services.auth_service.mark_as_sent"
                ) as mock_mark:

                    result = login(
                        db,
                        data
                    )

                    assert result == {
                        "access_token": "jwt-token",
                        "token_type": "bearer"
                    }

                    mock_verify.assert_called_once_with(
                        "password123",
                        "hashed_password"
                    )

                    mock_token.assert_called_once_with(
                        {"sub": "1"}
                    )

                    mock_mark.assert_called_once_with(
                        db,
                        1
                    )


def test_login_marks_pending_notifications_as_sent():
    db = Mock()

    user = Mock()
    user.id = 5
    user.password_hash = "hashed"

    data = Mock()
    data.email = "john@example.com"
    data.password = "password123"

    with patch(
        "app.services.auth_service.get_by_email",
        return_value=user
    ):
        with patch(
            "app.services.auth_service.verify_password",
            return_value=True
        ):
            with patch(
                "app.services.auth_service.create_access_token",
                return_value="token"
            ):
                with patch(
                    "app.services.auth_service.mark_as_sent"
                ) as mock_mark:

                    login(
                        db,
                        data
                    )

                    mock_mark.assert_called_once_with(
                        db,
                        5
                    )


def test_register_hashes_password_before_create():
    db = Mock()

    data = Mock()
    data.username = "john"
    data.email = "john@example.com"
    data.password = "plain_password"

    with patch(
        "app.services.auth_service.get_by_email",
        return_value=None
    ):
        with patch(
            "app.services.auth_service.hash_password",
            return_value="hashed_password"
        ):
            with patch(
                "app.services.auth_service.create_user"
            ) as mock_create:

                register(
                    db,
                    data
                )

                args = mock_create.call_args[0]

                assert args[2] == "hashed_password"
                assert args[2] != "plain_password"