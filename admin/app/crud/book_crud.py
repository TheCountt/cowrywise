from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.models import AdminBook
from typing import Optional
from app.schemas.schemas import BookCreate

def create_book(db: Session, book_data: BookCreate):
    """
    Create a new book and add it to the database with exception handling.
    """
    try:
        new_book = AdminBook(**book_data)
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of error
        print(f"Error creating book: {e}")  # Log the error
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the book. Please try again later."
        )


def get_available_books(db: Session):
    """
    Get all available books from the database with exception handling.
    """
    try:
        return db.query(AdminBook).filter(AdminBook.available == True).all()
    except SQLAlchemyError as e:
        print(f"Error fetching available books: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching available books. Please try again later."
        )


def get_unavailable_books(db: Session):
    """
    Get all unavailable books from the database with exception handling.
    """
    try:
        return db.query(AdminBook).filter(AdminBook.available == False).all()
    except SQLAlchemyError as e:
        print(f"Error fetching unavailable books: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching unavailable books. Please try again later."
        )


def get_all_books(db: Session):
    """
    Get all books from the database with exception handling.
    """
    try:
        return db.query(AdminBook).all()
    except SQLAlchemyError as e:
        print(f"Error fetching all books: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching all books. Please try again later."
        )


def delete_book_by_id(db: Session, book_id: str):
    """
    Deletes a book by its ID if it exists and is available for deletion.
    """
    try:
        book = db.query(AdminBook).filter(AdminBook.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found.")
        if book.available is False:
            raise HTTPException(status_code=400, detail="Cannot delete a book currently borrowed.")
        db.delete(book)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error deleting book by id: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting the book. Please try again later."
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please contact support."
        )


def delete_books_by_attribute(db: Session, publisher: Optional[str] = None, category: Optional[str] = None) -> int:
    """
    Deletes books filtered by either publisher or category with exception handling.

    Args:
        db (Session): Database session.
        publisher (Optional[str]): Publisher name to filter by.
        category (Optional[str]): Category name to filter by.

    Returns:
        int: The number of books deleted
    """
    try:
        if publisher:
            query = db.query(AdminBook).filter(AdminBook.publisher == publisher)
        elif category:
            query = db.query(AdminBook).filter(AdminBook.category == category)
        else:
            raise HTTPException(status_code=400, detail="No filter criteria provided.")
        
        deleted_count = query.delete(synchronize_session="fetch")
        db.commit()
        return deleted_count
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error deleting books by attribute: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting books by attribute. Please try again later."
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please contact support."
        )
