from typing import Optional

from fastapi import (FastAPI, Path, Query
, HTTPException)
from pydantic import BaseModel, Field
from starlette import status
app = FastAPI()


class Book:
    id: int
    title: str = Field(min_length = 3)
    author: str = Field(min_length = 1)
    description: str
    rating: int = Field(gt = 0, lt = 6)
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    description: str
    rating: int
    published_date: int = Field(gt = 1999, lt=2031)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Haider',
                'description': 'A new desc',
                'rating': 5,
                'published_date': 2029
            }
        }
BOOKS = [Book(1, "New", "Haider", "Okay", 4, 2029)]


@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/create-book", status_code = status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id+1
    else:
        book.id = 1
    return book

@app.get("/books/{book_id}", status_code = status.HTTP_200_OK)
async def get_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code = 404, detail = "Item not found")

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book

@app.delete("/books/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break

@app.get("/books/")
def read_book_by_rating(book_rating: int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return