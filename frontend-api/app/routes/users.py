from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud import user_crud
from app.db.database import get_db
from app.schemas.schemas import BookCreate, BookResponse

router = APIRouter()

# Endpoint to create a new book
@router.get("/enrolled-users", response_model=BookResponse)
def get_enrolled_users(db: Session = Depends(get_db)):
    """
   List of all users in the system.
    """
    users = user_crud.list_users(db)
    return users


@router.get("/borrowed")
def get_users_with_borrowed_books(db: Session = Depends(get_db)):
    """
   List of users and the books they have borrowed.
    """
    users_who_borrowed = user_crud.list_users_and_books_borrowed_by_them(db)
    return users_who_borrowed

