import os
import sys

# Add the parent directory to the path to import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Override the database configuration for serverless
from backend.app.database.database import Base
engine = create_engine('sqlite:///:memory:', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the in-memory database
Base.metadata.create_all(bind=engine)

def get_db_override():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import the create_app function from the backend
from backend.app.main import create_app

# Create the FastAPI app
app = create_app()

# Override the get_db dependency
from backend.app.database.database import get_db
app.dependency_overrides[get_db] = get_db_override

# Override CORS settings to allow requests from the same domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this would be restricted to your domain
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Export the app for Vercel serverless function
handler = app
