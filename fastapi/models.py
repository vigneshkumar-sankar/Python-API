from sqlalchemy import Column, Integer, String, Float
from database import Base
from pydantic import BaseModel
from typing import Optional


# --- SQLAlchemy Book model ---
class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    price = Column(Float)

# --- Pydantic schemas ---
class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float

    class Config:
        from_attributes = True

class BookCreate(BaseModel):
    title: str
    author: str
    price: float

class UserLogin(BaseModel):
    username: str
    password: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
