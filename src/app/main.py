"""
FastAPI main application for Library Management System.
This provides basic API endpoints to test the KAN-203 models and schemas.
"""
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from .database import get_db, create_tables
from .models.library import Library
from .models.book import Book
from .models.library_book import LibraryBook
from .schemas.library import LibraryCreate, LibraryUpdate, LibraryResponse, LibraryListResponse
from .schemas.book import BookCreate, BookUpdate, BookResponse, BookListResponse
from .schemas.library_book import LibraryBookCreate, LibraryBookUpdate, LibraryBookResponse, LibraryBookWithDetailsResponse
from .crud.library import LibraryCRUD
from .crud.book import BookCRUD
from .crud.library_book import LibraryBookCRUD

# Create FastAPI app
app = FastAPI(
    title="Library Management System API",
    description="API for testing KAN-203 SQLAlchemy models and Pydantic schemas",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    create_tables()

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Library Management System API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "libraries": "/api/v1/libraries",
            "books": "/api/v1/books",
            "library-books": "/api/v1/library-books",
            "docs": "/docs"
        }
    }

# Library endpoints
@app.post("/api/v1/libraries", response_model=LibraryResponse, status_code=201)
async def create_library(library: LibraryCreate, db: Session = Depends(get_db)):
    """Create a new library."""
    try:
        return LibraryCRUD.create(db, library)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/libraries/{library_id}", response_model=LibraryResponse)
async def get_library(library_id: int, db: Session = Depends(get_db)):
    """Get a library by ID."""
    library = LibraryCRUD.get_by_id(db, library_id)
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")
    return library

@app.get("/api/v1/libraries", response_model=LibraryListResponse)
async def get_libraries(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search term"),
    status: Optional[str] = Query(None, description="Library status"),
    dept: Optional[str] = Query(None, description="Department"),
    db: Session = Depends(get_db)
):
    """Get all libraries with pagination and filtering."""
    skip = (page - 1) * size
    libraries, total = LibraryCRUD.get_multi(
        db, skip=skip, limit=size, search=search, status=status, dept=dept
    )
    
    return LibraryListResponse(
        libraries=libraries,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )

@app.put("/api/v1/libraries/{library_id}", response_model=LibraryResponse)
async def update_library(
    library_id: int, 
    library_update: LibraryUpdate, 
    db: Session = Depends(get_db)
):
    """Update a library."""
    library = LibraryCRUD.update(db, library_id, library_update)
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")
    return library

@app.delete("/api/v1/libraries/{library_id}")
async def delete_library(library_id: int, db: Session = Depends(get_db)):
    """Delete a library."""
    if not LibraryCRUD.delete(db, library_id):
        raise HTTPException(status_code=404, detail="Library not found")
    return {"message": "Library deleted successfully"}

# Book endpoints
@app.post("/api/v1/books", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Create a new book."""
    try:
        return BookCRUD.create(db, book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a book by ID."""
    book = BookCRUD.get_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/api/v1/books/isbn/{isbn}", response_model=BookResponse)
async def get_book_by_isbn(isbn: str, db: Session = Depends(get_db)):
    """Get a book by ISBN."""
    book = BookCRUD.get_by_isbn(db, isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/api/v1/books", response_model=BookListResponse)
async def get_books(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search term"),
    category: Optional[str] = Query(None, description="Book category"),
    author: Optional[str] = Query(None, description="Book author"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    db: Session = Depends(get_db)
):
    """Get all books with pagination and filtering."""
    skip = (page - 1) * size
    books, total = BookCRUD.get_multi(
        db, skip=skip, limit=size, search=search, category=category, 
        author=author, min_price=min_price, max_price=max_price
    )
    
    return BookListResponse(
        books=books,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )

@app.put("/api/v1/books/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int, 
    book_update: BookUpdate, 
    db: Session = Depends(get_db)
):
    """Update a book."""
    book = BookCRUD.update(db, book_id, book_update)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/api/v1/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book."""
    if not BookCRUD.delete(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

# Library-Book mapping endpoints
@app.post("/api/v1/library-books", response_model=LibraryBookResponse, status_code=201)
async def create_library_book(mapping: LibraryBookCreate, db: Session = Depends(get_db)):
    """Create a new library-book mapping."""
    try:
        return LibraryBookCRUD.create(db, mapping)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/library-books/{mapping_id}", response_model=LibraryBookResponse)
async def get_library_book(mapping_id: int, db: Session = Depends(get_db)):
    """Get a library-book mapping by ID."""
    mapping = LibraryBookCRUD.get_by_id(db, mapping_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")
    return mapping

@app.get("/api/v1/libraries/{library_id}/books")
async def get_books_in_library(
    library_id: int, 
    status: Optional[str] = Query(None, description="Mapping status"),
    db: Session = Depends(get_db)
):
    """Get all books in a specific library."""
    books = LibraryBookCRUD.get_books_in_library(db, library_id, status)
    return {"library_id": library_id, "books": books}

@app.get("/api/v1/books/{book_id}/libraries")
async def get_libraries_for_book(
    book_id: int, 
    status: Optional[str] = Query(None, description="Mapping status"),
    db: Session = Depends(get_db)
):
    """Get all libraries that have a specific book."""
    libraries = LibraryBookCRUD.get_libraries_for_book(db, book_id, status)
    return {"book_id": book_id, "libraries": libraries}

@app.put("/api/v1/library-books/{mapping_id}", response_model=LibraryBookResponse)
async def update_library_book(
    mapping_id: int, 
    mapping_update: LibraryBookUpdate, 
    db: Session = Depends(get_db)
):
    """Update a library-book mapping."""
    mapping = LibraryBookCRUD.update(db, mapping_id, mapping_update)
    if not mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")
    return mapping

@app.delete("/api/v1/library-books/{mapping_id}")
async def delete_library_book(mapping_id: int, db: Session = Depends(get_db)):
    """Delete a library-book mapping."""
    if not LibraryBookCRUD.delete(db, mapping_id):
        raise HTTPException(status_code=404, detail="Mapping not found")
    return {"message": "Mapping deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.00.0", port=8000)
