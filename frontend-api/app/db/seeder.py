from sqlalchemy.orm import Session
from backend.app.models.models import AdminBook, AdminUser

def seed_db(db: Session):
    books = [
        {
            "title": "Clean Code",
            "author": "Robert C. Martin", 
            "publisher": "Prentice Hall", 
            "category": "Technology",
        },
            
        {
            "title": "1984", 
            "author": "George Orwell", 
            "publisher": "Secker & Warburg", 
            "category": "Fiction",
        }
    ]

    users = [
        {
            "email": "john@example.com",
            "firstname": "John",
            "lastname": "Doe",
        },

        {
            "email": "jane@example.com",
            "firstname": "Jane",
            "lastname": "Doe",
        }
    ]

    for book_data in books:
        book = AdminBook(**book_data)
        db.add(book)

    for user_data in users:
        user = AdminUser(**user_data)
        db.add(user)

    db.commit()
    