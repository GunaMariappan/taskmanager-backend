from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import os

host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "3306")
user = os.getenv("DB_USER", "root")
password = quote_plus(os.getenv("DB_PASSWORD", "sree@2022"))
db_name = os.getenv("DB_NAME", "taskmanager")

DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()