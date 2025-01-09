
from sqlalchemy import Column, Enum, String, Boolean, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from app.db.database import Base

# Book Model
class Book(Base):
    __tablename__ = "books"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    category = Column(String, nullable=False)
    available = Column(Boolean, default=True)
    due_date = Column(Date, nullable=True)

# User Roles Model
class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"

# User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    borrowed_books = relationship("BorrowedBook", back_populates="user")

# Borrowed Books Association
class BorrowedBook(Base):
    __tablename__ = "borrowed_books"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    book_id = Column(String, ForeignKey("books.id"), nullable=False)
    due_date = Column(Date, nullable=False)
    user = relationship("AdminUser", back_populates="borrowed_books")
    book = relationship("AdminBook")


