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
from .services.library_service import LibraryService
from .services.book_service import BookService
from .services.library_book_service import LibraryBookService

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
            "libraries": "/libraries",
            "books": "/books",
            "library-books": "/library-books",
            "docs": "/docs"
        }
    }

# KAN-204: Library CRUD Endpoints
@app.post("/libraries", status_code=201)
async def create_library(library: LibraryCreate, db: Session = Depends(get_db)):
    """
    Create a new library.
    
    Validates required fields and creates a library record in the database.
    Returns the created library ID and success message.
    """
    service = LibraryService(db)
    return service.create_library(library)

@app.get("/libraries")
async def get_libraries(db: Session = Depends(get_db)):
    """
    Get all libraries.
    
    Returns a list of all libraries in the database.
    """
    service = LibraryService(db)
    return service.get_all_libraries()

# KAN-205: Additional Library CRUD Endpoints
@app.get("/libraries/{library_id}")
async def get_library(library_id: int, db: Session = Depends(get_db)):
    """
    Get a library by ID.
    
    Returns the library object if found, 404 if not found.
    """
    service = LibraryService(db)
    return service.get_library_by_id(library_id)

@app.put("/libraries/{library_id}")
async def update_library(library_id: int, library_update: LibraryUpdate, db: Session = Depends(get_db)):
    """
    Update a library by ID.
    
    Supports partial updates - only provided fields will be updated.
    Returns success message if updated, 404 if not found.
    """
    service = LibraryService(db)
    return service.update_library(library_id, library_update)

@app.delete("/libraries/{library_id}")
async def delete_library(library_id: int, db: Session = Depends(get_db)):
    """
    Delete a library by ID.
    
    Cascade delete policy: All library-book mappings will be automatically deleted.
    Returns success message if deleted, 404 if not found.
    """
    service = LibraryService(db)
    return service.delete_library(library_id)

# KAN-206: Book CRUD Endpoints (Create/List)
@app.post("/books", status_code=201)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book.
    
    Validates required fields and creates a book record in the database.
    Returns the created book ID and success message.
    Enforces ISBN uniqueness at both DB and application level.
    """
    service = BookService(db)
    return service.create_book(book)

@app.get("/books")
async def get_books(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of books per page"),
    db: Session = Depends(get_db)
):
    """
    Get all books with pagination.
    
    Returns a paginated list of books in the database.
    """
    service = BookService(db)
    return service.get_books_paginated(page, limit)

# KAN-207: Additional Book CRUD Endpoints (Read/Update/Delete)
@app.get("/books/{book_id}")
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Get a book by ID.
    
    Returns the book object if found, 404 if not found.
    """
    service = BookService(db)
    return service.get_book_by_id(book_id)

@app.put("/books/{book_id}")
async def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """
    Update a book by ID.
    
    Supports partial updates - only provided fields will be updated.
    Respects unique ISBN constraint if ISBN is being updated.
    Returns success message if updated, 404 if not found.
    """
    service = BookService(db)
    return service.update_book(book_id, book_update)

@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book by ID.
    
    Cleanup policy: All library-book mappings will be automatically deleted.
    Returns success message if deleted, 404 if not found.
    """
    service = BookService(db)
    return service.delete_book(book_id)

# KAN-208: Library-Book Mapping Endpoints
@app.post("/library-books", status_code=201)
async def create_library_book_mapping(mapping: LibraryBookCreate, db: Session = Depends(get_db)):
    """
    Create a new library-book mapping.
    
    Links an existing book to a library with existence validation.
    Enforces unique (lib_id, book_id) constraint.
    Increments library count on successful mapping.
    """
    service = LibraryBookService(db)
    return service.create_mapping(mapping)

@app.get("/library-books")
async def get_library_book_mappings(db: Session = Depends(get_db)):
    """
    Get all library-book mappings.
    
    Returns a list of all library-book mappings in the database.
    """
    service = LibraryBookService(db)
    return service.get_all_mappings()

# KAN-209: Library-Book Mapping Detail/Update/Delete Endpoints
@app.get("/library-books/{mapping_id}")
async def get_library_book_mapping(mapping_id: int, db: Session = Depends(get_db)):
    """
    Get a library-book mapping by ID.
    
    Returns the mapping details if found, 404 if not found.
    """
    service = LibraryBookService(db)
    return service.get_mapping_by_id(mapping_id)

@app.put("/library-books/{mapping_id}")
async def update_library_book_mapping(mapping_id: int, mapping_update: LibraryBookUpdate, db: Session = Depends(get_db)):
    """
    Update a library-book mapping by ID.
    
    Supports status changes and adjusts library count accordingly.
    Returns success message if updated, 404 if not found.
    """
    service = LibraryBookService(db)
    return service.update_mapping(mapping_id, mapping_update)

@app.delete("/library-books/{mapping_id}")
async def delete_library_book_mapping(mapping_id: int, db: Session = Depends(get_db)):
    """
    Delete a library-book mapping by ID.
    
    Removes the relationship and updates library count.
    Returns success message if deleted, 404 if not found.
    """
    service = LibraryBookService(db)
    return service.delete_mapping(mapping_id)

# Legacy Book endpoints (keeping for backward compatibility)
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
