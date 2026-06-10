from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.project import ProjectStatus

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[ProjectStatus] = ProjectStatus.planning
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: ProjectStatus
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True