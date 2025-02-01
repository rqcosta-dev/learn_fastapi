from http import HTTPStatus
from fastapi.testclient import TestClient
from fast_zero.app import app


def test_read_root_success():
    client = TestClient(app)  # Create a TestClient instance | Arrange

    response = client.get("/")  # Make a GET request to the root path | Act

    assert (
        response.status_code == HTTPStatus.OK
    )  # Assert that the response status code is 200 OK
    assert response.json() == {
        "message": "Hello World!"
    }  # Assert that the response body is {"message": "Hello World!"}
