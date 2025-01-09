from sqlalchemy.orm import Session
from fastapi import  HTTPException
from app.models.models import AdminUser
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

# Fetch all enrolled users
def list_users(db: Session):
    return db.query(AdminUser).all()

def list_users_and_books_borrowed_by_them(db: Session):
    """
    List users and the books borrowed by them with exception handling.
    """
    try:
        users = db.query(AdminUser).all()
        result = []
        for user in users:
            borrowed_books = [
                {"book_id": borrow.book_id, "due_date": borrow.due_date} 
                for borrow in user.borrowed_books
            ]
            result.append({
                "user_id": user.id,
                "email": user.email,
                "borrowed_books": borrowed_books
            })
        return result
    except SQLAlchemyError as e:
        # Log the error for debugging purposes
        print(f"Database error occurred: {e}")
        # Raise an HTTPException with a meaningful message
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching users and their borrowed books. Please try again later."
        )