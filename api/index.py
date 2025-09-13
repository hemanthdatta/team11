import os
import sys
import logging
from datetime import datetime, timedelta
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to the path to import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    from typing import Optional, Dict, Any
    
    # Create a simple FastAPI app directly (not importing from backend)
    app = FastAPI(title="Micro-Entrepreneur API", docs_url="/api/docs")
    
    # Add exception handler for better error reporting
    @app.middleware("http")
    async def log_exceptions(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"detail": f"Server error: {str(e)}"}
            )
    
    # User schemas
    class UserCreate(BaseModel):
        name: str
        email: Optional[str] = None
        phone: Optional[str] = None
        user_id: str
        password: str

    class UserResponse(BaseModel):
        id: int = 1  # Hardcoded for testing
        name: str
        email: Optional[str] = None
        phone: Optional[str] = None
        user_id: str
        created_at: datetime = datetime.now()

    class LoginRequest(BaseModel):
        user_id: str
        password: str

    class Token(BaseModel):
        access_token: str
        token_type: str = "bearer"
    
    # Mock users database (in-memory)
    users_db = {}
    
    # Add signup endpoint
    @app.post("/auth/signup", response_model=UserResponse)
    async def signup(user: UserCreate):
        try:
            logger.info(f"Signup attempt for user_id: {user.user_id}")
            
            # Check if user exists
            if user.user_id in users_db:
                logger.warning(f"User {user.user_id} already exists")
                raise HTTPException(status_code=400, detail="User ID already registered")
            
            # Create user (simplified, no actual DB)
            new_user = {
                "id": len(users_db) + 1,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "user_id": user.user_id,
                "password": user.password,  # In production, hash this!
                "created_at": datetime.now().isoformat()
            }
            
            # Store in our mock DB
            users_db[user.user_id] = new_user
            logger.info(f"User {user.user_id} created successfully")
            
            # Return user data without password
            response_data = {k: v for k, v in new_user.items() if k != "password"}
            return response_data
        
        except HTTPException as he:
            # Re-raise HTTP exceptions
            raise he
        except Exception as e:
            # Log any other errors
            logger.error(f"Signup error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Signup error: {str(e)}")
    
    # Add login endpoint
    @app.post("/auth/login", response_model=Token)
    async def login(login_request: LoginRequest):
        try:
            logger.info(f"Login attempt for user_id: {login_request.user_id}")
            
            # Check if user exists and password matches
            if login_request.user_id not in users_db or users_db[login_request.user_id]["password"] != login_request.password:
                logger.warning(f"Invalid login for user_id: {login_request.user_id}")
                raise HTTPException(status_code=400, detail="Incorrect user ID or password")
            
            logger.info(f"Login successful for user_id: {login_request.user_id}")
            # Return a mock token
            return {"access_token": f"mock_token_{login_request.user_id}", "token_type": "bearer"}
        
        except HTTPException as he:
            # Re-raise HTTP exceptions
            raise he
        except Exception as e:
            # Log any other errors
            logger.error(f"Login error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")
    
    # Root endpoint for testing
    @app.get("/")
    async def root():
        return {"message": "API is working!"}

    # Health check endpoint for debugging
    @app.get("/api/health")
    async def health_check():
        return {
            "status": "ok", 
            "timestamp": datetime.now().isoformat(),
            "users_count": len(users_db),
            "python_path": sys.path
        }
    
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
    
except Exception as e:
    # Log startup errors
    print(f"Startup error: {str(e)}")
    
    # Create a minimal error-reporting app
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def error_root():
        return {"error": f"Failed to initialize API: {str(e)}"}
    
    handler = app
