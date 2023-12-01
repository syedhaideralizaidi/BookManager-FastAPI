from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
app = FastAPI()


class Book:
    id: int
    title: str = Field(min_length = 3)
    author: str = Field(min_length = 1)
    description: str
    rating: int = Field(gt = 0, lt = 6)

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    description: str
    rating: int

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Haider',
                'description': 'A new desc',
                'rating': 5
            }
        }
BOOKS =[
    Book(1, "New", "Haider", "Okay", 4)
]


@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id+1
    else:
        book.id  = 1
    return book

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            break