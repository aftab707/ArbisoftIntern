from app.models import User
from app.security import bootstrap_admin_user, verify_password


def test_bootstrap_admin_user_creates_admin_when_env_vars_set(db_session, monkeypatch):
    monkeypatch.setenv("ADMIN_EMAIL", "boss@example.com")
    monkeypatch.setenv("ADMIN_PASSWORD", "bosspass123")
    monkeypatch.setenv("ADMIN_NAME", "Boss")

    bootstrap_admin_user(db_session)

    admin = db_session.query(User).filter(User.email == "boss@example.com").first()
    assert admin is not None
    assert admin.role == "admin"
    assert verify_password("bosspass123", admin.hashed_password)


def test_bootstrap_admin_user_is_idempotent(db_session, monkeypatch):
    monkeypatch.setenv("ADMIN_EMAIL", "boss2@example.com")
    monkeypatch.setenv("ADMIN_PASSWORD", "bosspass123")

    bootstrap_admin_user(db_session)
    bootstrap_admin_user(db_session)

    count = db_session.query(User).filter(User.email == "boss2@example.com").count()
    assert count == 1


def test_bootstrap_admin_user_skips_when_env_vars_missing(db_session, monkeypatch):
    monkeypatch.delenv("ADMIN_EMAIL", raising=False)
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)

    bootstrap_admin_user(db_session)

    assert db_session.query(User).count() == 0
