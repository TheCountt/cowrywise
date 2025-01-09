from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.models import Book, User
from typing import Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy import update
from app.schemas.schemas import BookBase, BookResponse,  BorrowBookRequest

async def list_available_books(db: Session):
    """
    Get all available books from the database with exception handling.
    """
    try:
        return db.query(Book).filter(Book.available == True).all()
    except SQLAlchemyError as e:
        print(f"Error fetching available books: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching available books. Please try again later."
        )

# For high scalability and no concurrency issue, Atomic update implementation like below is the best 
async def borrow_book(request: BorrowBookRequest, db: Session):
    """Allows a user to borrow a book for a certain number of days."""

    result = db.execute(
        update(Book)
        .where(Book.id == request.book_id, Book.available == True)
        .values(
            available=False,
            due_date=datetime.now(timezone.utc) + timedelta(days=request.days)
        )
        .returning(Book.id)
    )

    updated_book_id = result.fetchone()
    if not updated_book_id:
        raise HTTPException(status_code=404, detail="Book not available")
    
    return {"message": "Book borrowed successfully", "book_id": updated_book_id[0]}


