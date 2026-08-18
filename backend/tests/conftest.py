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
        "/api/v1/auth/register",
        json={"name": "Aftab", "email": "aftab@example.com", "password": "secret123"},
    )
    return response.json()


@pytest.fixture
def auth_headers(client, existing_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": existing_user["email"], "password": "secret123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, db_session):
    from app.models import User
    from app.security import hash_password

    admin = User(
        name="Admin",
        email="admin@example.com",
        hashed_password=hash_password("adminpass123"),
        role="admin",
    )
    db_session.add(admin)
    db_session.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "adminpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_user_headers(client):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Other", "email": "other@example.com", "password": "secret123"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "other@example.com", "password": "secret123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
