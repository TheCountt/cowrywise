from app.crud.book_crud import create_book

def test_create_book(db):
    book_data = {
        "title": "Test Driven Development",
        "author": "Kent Beck",
        "publisher": "Ade Deji",
        "category": "Technology"
    }

    book = create_book(db, book_data)
    assert book.title == "Test Driven Development"
    assert book.author == "Kent Beck"