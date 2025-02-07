from http import HTTPStatus
from fast_zero.schemas import UserSchemaPublic


def test_read_root_success(client):
    response = client.get("/")  # Make a GET request to the root path | Act

    assert (
        response.status_code == HTTPStatus.OK
    )  # Assert that the response status code is 200 OK
    assert response.json() == {
        "message": "Hello World!"
    }  # Assert that the response body is {"message": "Hello World!"}


def test_response_html_success(client):
    response = client.get("/web-page")  # Make a GET request to the /web-page path | Act

    assert (
        response.status_code == HTTPStatus.OK
    )  # Assert that the response status code is 200 OK
    assert (
        response.headers["content-type"] == "text/html; charset=utf-8"
    )  # Assert that the response content type is text/html; charset=utf-8
    assert (
        "<h1>Hello World!</h1>" in response.text
    )  # Assert that the response body contains <h1>Hello World!</h1>


def test_create_user_success(client):
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "user@email.com",
            "password": "password",
        },
    )  # Make a POST request to the /users/ path | Act

    assert (
        response.status_code == HTTPStatus.CREATED
    )  # Assert that the response status code is 201 Created
    assert response.json() == {
        "id": 1,
        "username": "testuser",
        "email": "user@email.com",
    }


def test_create_user_integrity_error(client):
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "user@email.com",
            "password": "password",
        },
    )  # Make a POST request to the /users/ path | Act


def test_create_user_username_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": user.username,
            "email": "newemail@example.com",
            "password": "password",
        },
    )  # Make a POST request to the /users/ path | Act

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username already exists"}


def test_create_user_email_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "newuser",
            "email": user.email,
            "password": "password",
        },
    )  # Make a POST request to the /users/ path | Act

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email already exists"}


def test_read_user_empty(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_user_success(client, user):
    user_schema = UserSchemaPublic.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user_success(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},  # Add the Authorization header
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_update_integrity_error(client, user, token):
    # Create a new user
    client.post(
        "/users",
        json={
            "username": "fausto",
            "email": "fausto@example.com",
            "password": "secret",
        },
    )

    # Update the user
    response_update = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {"detail": "Username or Email already exists"}


def test_read_user_by_id_success(client, user):
    response = client.get(
        f"/users/{user.id}",
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }


def test_read_user_by_id_not_found(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user_success(client, user, token):
    # Delete the user
    response = client.delete(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted successfully"}


def test_get_access_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert token["token_type"] == "Bearer"


def test_get_access_token_invalid_user(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": "wrongpassword"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}
