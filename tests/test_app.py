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
