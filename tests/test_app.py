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
    # Assert that the response body is {"id": 1, "username": "testuser", "email": "
    # "user@email.com"}


def test_read_user_empty(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_user_success(client, user):
    user_schema = UserSchemaPublic.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user_success(client, user):
    response = client.put(
        "/users/1",
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


def test_update_integrity_error(client, user):
    # Criando um registro para "fausto"
    client.post(
        "/users",
        json={
            "username": "fausto",
            "email": "fausto@example.com",
            "password": "secret",
        },
    )

    # Alterando o user.username das fixture para fausto
    response_update = client.put(
        f"/users/{user.id}",
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {"detail": "Username or Email already exists"}


def test_update_user_not_found(client):
    response = client.put(
        "/users/1",
        json={
            "username": "testuser",
            "email": "user@email.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_read_user_by_id_success(client, user):
    response = client.get(f"/users/1")

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


def test_delete_user_success(client, user):
    # Delete the user
    response = client.delete(f"/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted successfully"}


def test_delete_user_not_found(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
