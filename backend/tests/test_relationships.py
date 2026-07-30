from app.models import Task, User


def test_tasks_created_for_a_user_are_returned_by_user_id_filter(client):
    user = client.post(
        "/api/v1/users/", json={"name": "Relationship User", "email": "rel@example.com"}
    ).json()

    task_a = client.post("/api/v1/tasks/", json={"title": "Task A", "user_id": user["id"]}).json()
    task_b = client.post("/api/v1/tasks/", json={"title": "Task B", "user_id": user["id"]}).json()

    assert task_a["user_id"] == user["id"]
    assert task_b["user_id"] == user["id"]

    response = client.get("/api/v1/tasks/", params={"user_id": user["id"]})
    titles = {task["title"] for task in response.json()}
    assert titles == {"Task A", "Task B"}


def test_user_task_orm_relationship_is_bidirectional(db_session):
    user = User(name="ORM User", email="orm@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    task = Task(title="ORM Task", user_id=user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.user.email == "orm@example.com"
    assert [t.title for t in user.tasks] == ["ORM Task"]


def test_deleting_a_user_cascades_to_their_tasks(db_session):
    user = User(name="Cascade User", email="cascade@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    db_session.add(Task(title="Orphaned on delete", user_id=user.id))
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    assert db_session.query(Task).count() == 0
