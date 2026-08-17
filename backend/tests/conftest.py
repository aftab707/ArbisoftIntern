import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401 ensures User/Task register on Base's registry
from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    # Not using `with TestClient(app) as c:` on purpose: entering that context
    # fires the app's lifespan, which calls init_db() against the real
    # sqlite:///./app.db engine, not this in-memory test one. Routing works
    # the same either way, and skipping lifespan keeps tests from touching
    # development data.
    return TestClient(app)


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def existing_user(client):
    response = client.post(
        "/api/v1/users/",
        json={"name": "Aftab", "email": "aftab@example.com"},
    )
    return response.json()
