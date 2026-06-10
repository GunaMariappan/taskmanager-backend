from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.utils.auth import verify_token

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_current_user(token: str, db: Session):
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    new_task = Task(**task.dict(), created_by=user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    token: str,
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    query = db.query(Task).filter(Task.created_by == user.id)
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    return query.all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, token: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    db_task = db.query(Task).filter(Task.id == task_id, Task.created_by == user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    db_task = db.query(Task).filter(Task.id == task_id, Task.created_by == user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}