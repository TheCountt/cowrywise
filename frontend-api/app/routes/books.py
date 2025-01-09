from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud import book_crud
from app.db.database import get_db
from app.schemas.schemas import BookCreate, BookResponse

router = APIRouter()

# Endpoint to create a new book
@router.post("/add", response_model=BookResponse, status_code=201)
def add_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """
    Creates a new book in the catalog.
    """
    add_book = book_crud.create_book(db, book_data)
    return add_book


# Endpoint to get all books
@router.get("/all-books", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    """
    Retrieves all  books regardless of status
    """
    get_books = book_crud.get_all_books(db)
    return get_books


# Endpoint to get all available books
@router.get("/available", response_model=List[BookResponse])
def get_available_books(db: Session = Depends(get_db)):
    """
    Retrieves all available books that are not currently borrowed.
    """
    available_books = book_crud.get_available_books(db)
    return available_books

# Endpoint to get all unavailable books
@router.get("/unavailable", response_model=List[BookResponse])
def get_unavailable_books(db: Session = Depends(get_db)):
    """
    Retrieves all unavailable books that are currently borrowed.
    """
    unavailable_books = book_crud.get_unavailable_books(db)
    return unavailable_books

# Endpoint to delete a book by ID
@router.delete("/{book_id}", response_model=bool)
def delete_book_by_id(book_id: str, db: Session = Depends(get_db)):
    """
    Deletes a specific book by ID.
    """
    success = book_crud.delete_book_by_id(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found",)
    return success

# Endpoint to delete books by publisher or category
@router.delete("/delete", response_model=int)
def delete_books_by_publisher_or_category(publisher: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Deletes books by publisher or category. One filter is required.
    """
    if not (publisher or category):
        raise HTTPException(status_code=400, detail="Either 'publisher' or 'category' must be specified",)
    
    deleted_count = book_crud.delete_books_by_attribute(db, publisher=publisher, category=category)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="No books found for the specified filter",)
    return deleted_count