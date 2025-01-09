from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    email: str
    first_name: str
    last_name: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    author: str
    publisher: str
    category: str
    

class BookResponse(BookBase):
    id: UUID
    available: bool
    due_date: Optional[datetime]

    class Config:
        orm_mode = True

class BorrowBookRequest(BaseModel):
    book_id: str = Field(..., description="The ID of the book to be borrowed")
    user_id: str = Field(..., description="The ID of the user borrowing the book")
    days: int = Field(..., gt=0, description="The number of days for which the book is being borrowed")