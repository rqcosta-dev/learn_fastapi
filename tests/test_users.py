from http import HTTPStatus
from fast_zero.schemas import UserSchemaPublic


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


def test_update_user_forbidden(client, user, token):
    response = client.put(
        f"/users/{user.id + 1}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        "detail": "You don't have permission to update this user"
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


def test_delete_user_forbidden(client, user, token):
    # Delete the user
    response = client.delete(
        f"/users/{user.id + 1}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        "detail": "You don't have permission to delete this user"
    }
