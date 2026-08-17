from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task, User
from app.schemas import TaskCreate, TaskResponse

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


def _get_task_or_404(task_id: int, db: Session) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


def _ensure_user_exists(user_id: int, db: Session) -> None:
    if db.get(User, user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> Task:
    _ensure_user_exists(payload.user_id, db)

    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    status_filter: str | None = Query(default=None, alias="status"),
    user_id: int | None = Query(default=None),
) -> list[Task]:
    query = db.query(Task)
    if status_filter is not None:
        query = query.filter(Task.status == status_filter)
    if user_id is not None:
        query = query.filter(Task.user_id == user_id)
    return query.order_by(Task.id).all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)) -> Task:
    return _get_task_or_404(task_id, db)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskCreate, db: Session = Depends(get_db)) -> Task:
    task = _get_task_or_404(task_id, db)
    _ensure_user_exists(payload.user_id, db)

    for field, value in payload.model_dump().items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    task = _get_task_or_404(task_id, db)
    db.delete(task)
    db.commit()
