from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.models import User as UserModel
from app.schemas.schemas import UserCreate, User as UserSchema, UserUpdate, PasswordChangeRequest
from app.schemas.login import LoginRequest
from app.core.security import get_password_hash, create_access_token, verify_password, get_current_user_id
from datetime import timedelta
from typing import Dict, Any

router = APIRouter()

@router.post("/signup", response_model=UserSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(UserModel).filter(UserModel.user_id == user.user_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User ID already registered")
    
    # Check if email is already registered
    if user.email:
        db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    db_user = UserModel(
        name=user.name,
        email=user.email,
        phone=user.phone,
        user_id=user.user_id
    )
    db_user.set_password(user.password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login")
def login_user(login_request: LoginRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    user_id = login_request.user_id
    password = login_request.password
    
    # Find user by user_id
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect user ID or password")
    
    # Verify password
    if not verify_password(password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect user ID or password")
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.user_id}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=UserSchema)
def get_user_profile(current_user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.user_id == current_user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/profile", response_model=UserSchema)
def update_user_profile(user_update: UserUpdate, current_user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.user_id == current_user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields if provided
    if user_update.name is not None:
        db_user.name = user_update.name
    if user_update.email is not None:
        # Check if email is already taken by another user
        existing_user = db.query(UserModel).filter(
            UserModel.email == user_update.email,
            UserModel.id != db_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        db_user.email = user_update.email
    if user_update.phone is not None:
        # Check if phone is already taken by another user
        existing_user = db.query(UserModel).filter(
            UserModel.phone == user_update.phone,
            UserModel.id != db_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone number already registered")
        db_user.phone = user_update.phone
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/change-password")
def change_password(password_request: PasswordChangeRequest, current_user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.user_id == current_user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not verify_password(password_request.current_password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
    db_user.set_password(password_request.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}