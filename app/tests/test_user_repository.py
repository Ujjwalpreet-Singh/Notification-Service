import pytest
from unittest.mock import Mock

from app.repositories.user_repository import (
    create_user,
    get_by_email,
    get_by_id
)


def test_create_user_success():
    db = Mock()

    user = create_user(
        db=db,
        username="john",
        password_hash="hashed_password",
        email="john@example.com"
    )

    assert user.username == "john"
    assert user.password_hash == "hashed_password"
    assert user.email == "john@example.com"

    db.add.assert_called_once_with(user)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)


def test_get_by_email_returns_user():
    db = Mock()

    expected_user = Mock()
    expected_user.email = "john@example.com"

    query = Mock()

    db.query.return_value = query
    query.filter.return_value.first.return_value = expected_user

    result = get_by_email(
        db=db,
        email="john@example.com"
    )

    assert result == expected_user
    assert result.email == "john@example.com"


def test_get_by_email_returns_none_when_missing():
    db = Mock()

    query = Mock()

    db.query.return_value = query
    query.filter.return_value.first.return_value = None

    result = get_by_email(
        db=db,
        email="missing@example.com"
    )

    assert result is None


def test_get_by_id_returns_user():
    db = Mock()

    expected_user = Mock()
    expected_user.id = 1

    query = Mock()

    db.query.return_value = query
    query.filter.return_value.first.return_value = expected_user

    result = get_by_id(
        db=db,
        user_id=1
    )

    assert result == expected_user
    assert result.id == 1


def test_get_by_id_returns_none_when_missing():
    db = Mock()

    query = Mock()

    db.query.return_value = query
    query.filter.return_value.first.return_value = None

    result = get_by_id(
        db=db,
        user_id=999
    )

    assert result is None


def test_create_user_commit_failure():
    db = Mock()

    db.commit.side_effect = Exception("Database Error")

    with pytest.raises(Exception):
        create_user(
            db=db,
            username="john",
            password_hash="hashed",
            email="john@example.com"
        )

    db.add.assert_called_once()
    db.commit.assert_called_once()