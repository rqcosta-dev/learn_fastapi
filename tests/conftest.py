import pytest

from testcontainers.postgres import PostgresContainer
from fastapi.testclient import TestClient
from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import table_registry
from fast_zero.security import get_password_hash
from tests.factories import UserFactory


@pytest.fixture()
def client(session):
    # Create a TestClient instance to interact with the FastAPI application
    # Arrange
    def override_get_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = override_get_session
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def engine():
    # Create a Postgres container for the duration of the test session
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        _engine = create_engine(postgres.get_connection_url())
        with _engine.begin():
            yield _engine


@pytest.fixture()
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time
        if hasattr(target, "updated_at"):
            target.updated_at = time

    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session):
    password = "testtest"
    user = UserFactory(password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password
    return user


@pytest.fixture
def other_user(session):
    password = "testtest"
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.clean_password},
    )
    return response.json()["access_token"]
