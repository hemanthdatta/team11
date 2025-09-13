from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add the parent directory to the path to import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the create_app function from the backend
from backend.app.main import create_app

# Create the FastAPI app
app = create_app()

# Override CORS settings to allow requests from the same domain
# This is important for Vercel deployment where frontend and backend are on the same domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this would be restricted to your domain
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Export the app for Vercel serverless function
handler = app
