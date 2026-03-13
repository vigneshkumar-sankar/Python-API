from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import BookCreate, UserLogin, BookUpdate
import crud
from fastapi.encoders import jsonable_encoder

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dummy users
users_db = [
    {"username": "admin", "password": "admin123"},
    {"username": "test", "password": "test123"}
]

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------- Common Response Function --------


def api_response(status: str, code: int, message: str, data=None):
    return JSONResponse(
        status_code=code,
        content={
            "status": status,
            "code": code,
            "message": message,
            "data": jsonable_encoder(data)
        }
    )


# --------- User Login ----------
@app.post("/login")
def login(user: UserLogin):

    for u in users_db:
        if u["username"] == user.username and u["password"] == user.password:

            return api_response(
                "success",
                200,
                f"Login Successful. Welcome {user.username}!",
                {"name": user.username}
            )

    return api_response(
        "fail",
        401,
        "Invalid username or password",
        None
    )


# --------- GET all books ----------
@app.get("/books")
def read_books(db: Session = Depends(get_db)):

    books = crud.get_books(db)

    data = []
    for book in books:
        data.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "price": book.price
        })

    return api_response(
        "success",
        200,
        "Books fetched successfully",
        data
    )

# --------- GET book by ID ----------
@app.get("/books/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):

    db_book = crud.get_book(db, book_id)

    if db_book is None:
        return api_response(
            "fail",
            404,
            "Book not found",
            None
        )

    data = {
        "id": db_book.id,
        "title": db_book.title,
        "author": db_book.author,
        "price": db_book.price
    }

    return api_response(
        "success",
        200,
        "Book fetched successfully",
        data
    )


# --------- CREATE a new book ----------
@app.post("/books")
def add_book(book: BookCreate, db: Session = Depends(get_db)):

    new_book = crud.create_book(db, book)

    data = {
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author,
        "price": new_book.price
    }

    return api_response(
        "success",
        201,
        "Book created successfully",
        data
    )


# --------- UPDATE a book ----------
@app.put("/books/{book_id}")
def edit_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):

    db_book = crud.update_book(db, book_id, book)

    if not db_book:
        return api_response(
            "fail",
            404,
            "Book not found",
            None
        )

    return api_response(
        "success",
        200,
        "Book updated successfully",
        db_book
    )


# --------- DELETE a book ----------
@app.delete("/books/{book_id}")
def remove_book(book_id: int, db: Session = Depends(get_db)):

    db_book = crud.delete_book(db, book_id)

    if db_book is None:
        return api_response(
            "fail",
            404,
            "Book not found",
            None
        )

    return api_response(
        "success",
        200,
        f"Book '{db_book.title}' deleted successfully",
        None
    )