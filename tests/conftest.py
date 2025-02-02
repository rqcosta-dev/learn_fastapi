import pytest
from fastapi.testclient import TestClient
from fast_zero.app import app


@pytest.fixture()
def client():
    # Create a TestClient instance to interact with the FastAPI application
    # Arrange
    return TestClient(app)
