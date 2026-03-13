from sqlalchemy.orm import Session
from models import BookDB, BookCreate
# models.py
from pydantic import BaseModel
from typing import Optional

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None

# Get all books
def get_books(db: Session):
    return db.query(BookDB).all()

# Get book by ID
def get_book(db: Session, book_id: int):
    return db.query(BookDB).filter(BookDB.id == book_id).first()

# Create a new book
def create_book(db: Session, book: BookCreate):
    db_book = BookDB(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Update a book
def update_book(db: Session, book_id: int, book):
    db_book = get_book(db, book_id)

    if not db_book:
        return None

    update_data = book.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)

    return db_book

# Delete a book
def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book