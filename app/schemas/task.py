from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.todo
    priority: Optional[TaskPriority] = TaskPriority.medium
    due_date: Optional[datetime] = None
    project_id: int
    assigned_to: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime] = None
    project_id: int
    assigned_to: Optional[int] = None
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True