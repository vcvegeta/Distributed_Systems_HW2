# ============================================================
# Part 2 - FastAPI Book Management REST API
# This server provides CRUD endpoints for managing a list of
# books, along with search functionality. The frontend is
# served from the static/ directory.
# ============================================================

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import webbrowser

app = FastAPI(title="Book Management API", version="1.0.0")

# Mount the static directory so HTML, CSS, and JS files are served correctly
app.mount("/static", StaticFiles(directory="static"), name="static")


# ---- Pydantic models for request / response validation ----

class Book(BaseModel):
    """Represents a book with an auto-generated id, title, and author."""
    id: int
    title: str
    author: str


class BookCreate(BaseModel):
    """Schema used when creating a new book (id is generated server-side)."""
    title: str
    author: str


class BookUpdate(BaseModel):
    """Schema used when updating an existing book's title and/or author."""
    title: str
    author: str


# ---- In-memory book storage with sample data ----

books: List[Book] = [
    Book(id=1, title="To Kill a Mockingbird", author="Harper Lee"),
    Book(id=2, title="1984", author="George Orwell"),
    Book(id=3, title="The Great Gatsby", author="F. Scott Fitzgerald"),
]


# ---- Serve the main HTML page ----

@app.get("/")
async def read_root():
    """Return the single-page frontend."""
    return FileResponse("static/index.html")


# ============================================================
# Part 2 – Q1: Add a new book
# The user enters a Book Title and Author Name. On submission
# the book is created and the updated list is shown.
# ============================================================

@app.post("/api/books", response_model=Book, status_code=201)
async def create_book(book_data: BookCreate):
    """Create a new book – accepts JSON with 'title' and 'author' fields."""
    # Validate that neither field is blank
    if not book_data.title.strip():
        raise HTTPException(status_code=400, detail="Book title is required")
    if not book_data.author.strip():
        raise HTTPException(status_code=400, detail="Author name is required")

    # Auto-generate the next ID based on current maximum
    new_id = max([b.id for b in books], default=0) + 1
    new_book = Book(id=new_id, title=book_data.title, author=book_data.author)
    books.append(new_book)

    print(f"[CREATE] Added book: {new_book}")
    return new_book


# ============================================================
# Part 2 – Q2: Update a book by ID
# Example: update book with ID 1 to title "Harry Potter",
# author "J.K. Rowling". After submission the updated list
# is displayed.
# ============================================================

@app.put("/api/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book_data: BookUpdate):
    """Update an existing book's title and author by its ID."""
    # Find the book with the given ID
    book = next((b for b in books if b.id == book_id), None)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book_data.title.strip():
        raise HTTPException(status_code=400, detail="Book title is required")
    if not book_data.author.strip():
        raise HTTPException(status_code=400, detail="Author name is required")

    # Apply the updates
    book.title = book_data.title
    book.author = book_data.author
    print(f"[UPDATE] Updated book ID {book_id}: {book}")
    return book


# ============================================================
# Part 2 – Q3: Delete the book with the highest ID
# After deletion the home view refreshes to show the
# remaining books.
# ============================================================

@app.delete("/api/books/highest", status_code=204)
async def delete_highest_book():
    """Delete the book that currently has the highest ID."""
    global books
    if not books:
        raise HTTPException(status_code=404, detail="No books to delete")

    # Identify the book with the maximum ID value
    highest_book = max(books, key=lambda b: b.id)
    books = [b for b in books if b.id != highest_book.id]
    print(f"[DELETE] Removed book with highest ID: {highest_book}")
    return None


# ============================================================
# Part 2 – Q4: Search for books by title
# The user types a search query and only matching books are
# returned (case-insensitive partial match).
# ============================================================

@app.get("/api/books", response_model=List[Book])
async def get_books(response: Response, search: Optional[str] = Query(default=None)):
    """Return all books, or filter by title if a search query is provided."""
    # Prevent browser caching so the list always reflects current data
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    if search and search.strip():
        # Case-insensitive partial match on the book title
        query = search.strip().lower()
        filtered = [b for b in books if query in b.title.lower()]
        return filtered

    return books


@app.get("/api/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    """Retrieve a single book by its ID."""
    book = next((b for b in books if b.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# ---- Start the server ----

if __name__ == "__main__":
    webbrowser.open("http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
