# show_books.py
from database import SessionLocal
from models import BookDB

def show_books():
    db = SessionLocal()
    books = db.query(BookDB).all()
    if not books:
        print("No books found.")
    else:
        for book in books:
            print(f"{book.id} | {book.title} | {book.author} | {book.price}")
    db.close()

if __name__ == "__main__":
    show_books()