from sqlalchemy.orm import Session
from fastapi import  HTTPException
from app.models.models import  User
from app.schemas.schemas import UserCreate, UserResponse
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

# Enroll users
async def enroll_user(user: UserCreate, db: Session):

    """
    Check if email exists first
    """

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    """
    Enroll new user into the system
    """

    try:
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of error
        print(f"Error enrolling user: {e}")  # Log the error
        raise HTTPException(
            status_code=500,
            detail="An error occurred while enrolling user. Contact Admin."
        )