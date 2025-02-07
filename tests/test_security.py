from http import HTTPStatus
from jwt import decode as jwt_decode
from fast_zero.security import create_access_token, SECRET_KEY
from fastapi.exceptions import HTTPException


def test_jwt():
    data = {"test": "test"}
    token = create_access_token(data)

    decoded = jwt_decode(token, SECRET_KEY, algorithms=["HS256"])

    assert decoded["test"] == data["test"]
    assert decoded["exp"]


def test_jwt_invalid_token(client):
    response = client.delete(
        "/users/1", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_test_get_current_user_not_found(client):
    data = {"no-email": "test"}
    token = create_access_token(data)

    response = client.delete(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_get_current_user_does_not_exists(client):
    data = {"sub": "test@test"}
    token = create_access_token(data)

    response = client.delete(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
