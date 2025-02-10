from http import HTTPStatus
from freezegun import freeze_time


def test_get_access_token(client, user):
    response = client.post(
        "auth/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert token["token_type"] == "Bearer"


def test_get_access_token_invalid_user(client, user):
    response = client.post(
        "auth/token",
        data={"username": user.email, "password": "wrongpassword"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}


def test_token_expired(client, user):
    with freeze_time("2025-01-01 00:00:00"):
        response = client.post(
            "auth/token",
            data={"username": user.email, "password": user.clean_password},
        )

    assert response.status_code == HTTPStatus.OK

    token = response.json()["access_token"]

    with freeze_time("2025-01-01 00:30:01"):
        response = client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": "bob",
                "email": "wrong@email.com",
                "password": "newpassword",
            },
        )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_refresh_token(client, token):
    response = client.post(
        "auth/refresh_token",
        headers={"Authorization": f"Bearer {token}"},
    )
    result = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in result
    assert result["token_type"] == "Bearer"


def test_token_expired_dont_refresh(client, user):
    with freeze_time("2025-01-01 00:00:00"):
        response = client.post(
            "auth/token",
            data={"username": user.email, "password": user.clean_password},
        )

    assert response.status_code == HTTPStatus.OK

    token = response.json()["access_token"]

    with freeze_time("2025-01-01 00:30:01"):
        response = client.post(
            "auth/refresh_token",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
