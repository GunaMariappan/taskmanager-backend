from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.utils.auth import verify_token

router = APIRouter(prefix="/projects", tags=["Projects"])

def get_current_user(token: str, db: Session):
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    new_project = Project(**project.dict(), owner_id=user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/", response_model=List[ProjectResponse])
def get_projects(token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    projects = db.query(Project).filter(Project.owner_id == user.id).all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, token: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    db_project = db.query(Project).filter(Project.id == project_id, Project.owner_id == user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project.dict(exclude_unset=True).items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/{project_id}")
def delete_project(project_id: int, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    db_project = db.query(Project).filter(Project.id == project_id, Project.owner_id == user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted successfully"}