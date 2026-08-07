def test_register_returns_201_and_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"name": "Aftab", "email": "aftab@example.com", "password": "secret123"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "aftab@example.com"
    assert body["role"] == "user"
    assert "password" not in body
    assert "hashed_password" not in body


def test_register_duplicate_email_returns_400(client, existing_user):
    response = client.post(
        "/api/v1/auth/register",
        json={"name": "Someone Else", "email": existing_user["email"], "password": "secret123"},
    )

    assert response.status_code == 400


def test_register_short_password_returns_422(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"name": "Aftab", "email": "aftab@example.com", "password": "short"},
    )

    assert response.status_code == 422


def test_login_success_returns_token(client, existing_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": existing_user["email"], "password": "secret123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password_returns_401(client, existing_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": existing_user["email"], "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_login_unknown_email_returns_401(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "whatever"},
    )

    assert response.status_code == 401


def test_protected_route_without_token_returns_401(client):
    response = client.get("/api/v1/tasks/")

    assert response.status_code == 401


def test_protected_route_with_invalid_token_returns_401(client):
    response = client.get(
        "/api/v1/tasks/", headers={"Authorization": "Bearer not-a-real-token"}
    )

    assert response.status_code == 401


def test_full_happy_path_register_login_and_manage_tasks(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={"name": "Happy Path", "email": "happy@example.com", "password": "secret123"},
    )
    assert register_response.status_code == 201
    user_id = register_response.json()["id"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "happy@example.com", "password": "secret123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/api/v1/tasks/", json={"title": "Ship the feature"}, headers=headers
    )
    assert create_response.status_code == 201
    task = create_response.json()
    assert task["user_id"] == user_id

    get_response = client.get(f"/api/v1/tasks/{task['id']}", headers=headers)
    assert get_response.status_code == 200

    update_response = client.put(
        f"/api/v1/tasks/{task['id']}",
        json={"title": "Ship the feature", "status": "done"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "done"

    delete_response = client.delete(f"/api/v1/tasks/{task['id']}", headers=headers)
    assert delete_response.status_code == 204

    final_get = client.get(f"/api/v1/tasks/{task['id']}", headers=headers)
    assert final_get.status_code == 404
