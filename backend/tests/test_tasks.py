def test_create_task_with_valid_data_returns_201(client, existing_user):
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "Write tests", "user_id": existing_user["id"]},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["status"] == "pending"
    assert body["priority"] == "medium"
    assert body["user_id"] == existing_user["id"]
    assert "id" in body


def test_create_task_missing_title_returns_422(client, existing_user):
    response = client.post(
        "/api/v1/tasks/",
        json={"user_id": existing_user["id"]},
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]


def test_create_task_with_wrong_field_type_returns_422(client, existing_user):
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "Bad user id", "user_id": "not-a-number"},
    )

    assert response.status_code == 422


def test_create_task_with_unknown_user_returns_404(client):
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "Orphan task", "user_id": 999},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_list_tasks_returns_all_created_tasks(client, existing_user):
    client.post("/api/v1/tasks/", json={"title": "Task A", "user_id": existing_user["id"]})
    client.post("/api/v1/tasks/", json={"title": "Task B", "user_id": existing_user["id"]})

    response = client.get("/api/v1/tasks/")

    assert response.status_code == 200
    titles = [task["title"] for task in response.json()]
    assert titles == ["Task A", "Task B"]


def test_list_tasks_filters_by_status_and_user_id(client, existing_user):
    client.post(
        "/api/v1/tasks/",
        json={"title": "Done task", "user_id": existing_user["id"], "status": "done"},
    )
    client.post(
        "/api/v1/tasks/",
        json={"title": "Pending task", "user_id": existing_user["id"]},
    )

    by_status = client.get("/api/v1/tasks/", params={"status": "done"})
    assert by_status.status_code == 200
    assert [t["title"] for t in by_status.json()] == ["Done task"]

    by_unknown_user = client.get("/api/v1/tasks/", params={"user_id": 999})
    assert by_unknown_user.status_code == 200
    assert by_unknown_user.json() == []


def test_get_single_task_returns_it(client, existing_user):
    created = client.post(
        "/api/v1/tasks/", json={"title": "Fetch me", "user_id": existing_user["id"]}
    ).json()

    response = client.get(f"/api/v1/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == "Fetch me"


def test_get_task_not_found_returns_404(client):
    response = client.get("/api/v1/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task_status_and_details(client, existing_user):
    created = client.post(
        "/api/v1/tasks/", json={"title": "Original", "user_id": existing_user["id"]}
    ).json()

    response = client.put(
        f"/api/v1/tasks/{created['id']}",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "status": "in_progress",
            "priority": "high",
            "user_id": existing_user["id"],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Updated title"
    assert body["description"] == "Updated description"
    assert body["status"] == "in_progress"
    assert body["priority"] == "high"


def test_update_task_not_found_returns_404(client, existing_user):
    response = client.put(
        "/api/v1/tasks/999",
        json={"title": "x", "user_id": existing_user["id"]},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task_then_404_on_subsequent_requests(client, existing_user):
    created = client.post(
        "/api/v1/tasks/", json={"title": "Temporary", "user_id": existing_user["id"]}
    ).json()
    task_id = created["id"]

    delete_response = client.delete(f"/api/v1/tasks/{task_id}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404

    second_delete = client.delete(f"/api/v1/tasks/{task_id}")
    assert second_delete.status_code == 404
