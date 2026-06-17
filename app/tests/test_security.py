from jose import jwt
from unittest.mock import patch

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)


def test_hash_password():
    password = "password123"

    hashed = hash_password(password)

    assert hashed != password
    assert isinstance(hashed, str)


def test_verify_password_success():
    password = "password123"

    hashed = hash_password(password)

    assert verify_password(
        password,
        hashed
    ) is True


def test_verify_password_failure():
    password = "password123"

    hashed = hash_password(password)

    assert verify_password(
        "wrong_password",
        hashed
    ) is False


def test_create_access_token():
    with patch(
        "app.core.security.settings.SECRET_KEY",
        "test-secret"
    ):
        with patch(
            "app.core.security.settings.ACCESS_TOKEN_EXPIRE_MINUTES",
            30
        ):
            token = create_access_token(
                {"sub": "1"}
            )

            assert isinstance(token, str)
            assert len(token) > 0


def test_decode_access_token_success():
    secret = "test-secret"

    token = jwt.encode(
        {"sub": "1"},
        secret,
        algorithm="HS256"
    )

    with patch(
        "app.core.security.settings.SECRET_KEY",
        secret
    ):
        payload = decode_access_token(token)

        assert payload is not None
        assert payload["sub"] == "1"


def test_decode_access_token_invalid_token():
    with patch(
        "app.core.security.settings.SECRET_KEY",
        "test-secret"
    ):
        payload = decode_access_token(
            "invalid.jwt.token"
        )

        assert payload is None


def test_create_and_decode_access_token():
    with patch(
        "app.core.security.settings.SECRET_KEY",
        "test-secret"
    ):
        with patch(
            "app.core.security.settings.ACCESS_TOKEN_EXPIRE_MINUTES",
            30
        ):
            token = create_access_token(
                {"sub": "123"}
            )

            payload = decode_access_token(
                token
            )

            assert payload is not None
            assert payload["sub"] == "123"
            assert "exp" in payload


def test_hash_password_generates_different_hashes():
    password = "password123"

    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2


def test_verify_password_with_multiple_hashes():
    password = "password123"

    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert verify_password(password, hash1)
    assert verify_password(password, hash2)