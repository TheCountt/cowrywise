from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    category: str
    available: Optional[bool] = True

class BookOut(BaseModel):
    id: str
    title: str
    author: str
    publisher: str
    category: str
    available: bool
    due_date: Optional[datetime]

class AdminUserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str

class BookResponse(BookCreate):
    id: int

    class Config:
        orm_mode = True