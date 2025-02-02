from http import HTTPStatus


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


def test_read_user_success(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [{"id": 1, "username": "testuser", "email": "user@email.com"}]
    }


def test_update_user_success(client):
    response = client.put(
        "/users/1",
        json={
            "username": "testuser",
            "email": "user@email.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "testuser",
        "email": "user@email.com",
    }


def test_update_user_not_found(client):
    response = client.put(
        "/users/2",
        json={
            "username": "testuser",
            "email": "user@email.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_read_user_by_id_success(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "testuser",
        "email": "user@email.com",
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "testuser",
        "email": "user@email.com",
    }


def test_read_user_by_id_not_found(client):
    response = client.get("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user_success(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted successfully"}


def test_delete_user_not_found(client):
    response = client.delete("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
