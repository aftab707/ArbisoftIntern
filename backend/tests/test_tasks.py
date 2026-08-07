def test_create_task_with_valid_data_returns_201(client, existing_user, auth_headers):
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "Write tests"},
        headers=auth_headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["status"] == "pending"
    assert body["priority"] == "medium"
    assert body["user_id"] == existing_user["id"]
    assert "id" in body


def test_create_task_missing_title_returns_422(client, auth_headers):
    response = client.post(
        "/api/v1/tasks/",
        json={},
        headers=auth_headers,
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]


def test_create_task_without_auth_returns_401(client):
    response = client.post("/api/v1/tasks/", json={"title": "No auth"})

    assert response.status_code == 401


def test_list_tasks_returns_all_created_tasks(client, auth_headers):
    client.post("/api/v1/tasks/", json={"title": "Task A"}, headers=auth_headers)
    client.post("/api/v1/tasks/", json={"title": "Task B"}, headers=auth_headers)

    response = client.get("/api/v1/tasks/", headers=auth_headers)

    assert response.status_code == 200
    titles = [task["title"] for task in response.json()]
    assert titles == ["Task A", "Task B"]


def test_list_tasks_filters_by_status_and_user_id(client, existing_user, auth_headers):
    client.post(
        "/api/v1/tasks/",
        json={"title": "Done task", "status": "done"},
        headers=auth_headers,
    )
    client.post(
        "/api/v1/tasks/",
        json={"title": "Pending task"},
        headers=auth_headers,
    )

    by_status = client.get("/api/v1/tasks/", params={"status": "done"}, headers=auth_headers)
    assert by_status.status_code == 200
    assert [t["title"] for t in by_status.json()] == ["Done task"]

    by_unknown_user = client.get(
        "/api/v1/tasks/", params={"user_id": 999}, headers=auth_headers
    )
    assert by_unknown_user.status_code == 200
    assert by_unknown_user.json() == []


def test_get_single_task_returns_it(client, auth_headers):
    created = client.post(
        "/api/v1/tasks/", json={"title": "Fetch me"}, headers=auth_headers
    ).json()

    response = client.get(f"/api/v1/tasks/{created['id']}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["title"] == "Fetch me"


def test_get_task_not_found_returns_404(client, auth_headers):
    response = client.get("/api/v1/tasks/999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task_status_and_details(client, auth_headers):
    created = client.post(
        "/api/v1/tasks/", json={"title": "Original"}, headers=auth_headers
    ).json()

    response = client.put(
        f"/api/v1/tasks/{created['id']}",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "status": "in_progress",
            "priority": "high",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Updated title"
    assert body["description"] == "Updated description"
    assert body["status"] == "in_progress"
    assert body["priority"] == "high"


def test_update_task_not_found_returns_404(client, auth_headers):
    response = client.put(
        "/api/v1/tasks/999",
        json={"title": "x"},
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task_owned_by_another_user_returns_403(client, auth_headers, other_user_headers):
    created = client.post(
        "/api/v1/tasks/", json={"title": "Owned by first user"}, headers=auth_headers
    ).json()

    response = client.put(
        f"/api/v1/tasks/{created['id']}",
        json={"title": "Hijacked"},
        headers=other_user_headers,
    )

    assert response.status_code == 403


def test_delete_task_owned_by_another_user_returns_403(client, auth_headers, other_user_headers):
    created = client.post(
        "/api/v1/tasks/", json={"title": "Owned by first user"}, headers=auth_headers
    ).json()

    response = client.delete(f"/api/v1/tasks/{created['id']}", headers=other_user_headers)

    assert response.status_code == 403


def test_delete_task_then_404_on_subsequent_requests(client, auth_headers):
    created = client.post(
        "/api/v1/tasks/", json={"title": "Temporary"}, headers=auth_headers
    ).json()
    task_id = created["id"]

    delete_response = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404

    second_delete = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert second_delete.status_code == 404
