from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth
from app.routers import projects
from app.routers import tasks

# Import models so tables get created
from app.models import user, project, task

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="Enterprise Task Management Platform",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "https://famous-melomakarona-acbf6a.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Task Manager API is running! 🚀"}
