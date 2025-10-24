"""
Book Service Layer

This module contains the business logic for book operations.
It acts as an intermediary between the API endpoints and the CRUD layer.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..crud.book import BookCRUD
from ..schemas.book import BookCreate, BookUpdate, BookResponse


class BookService:
    """Service class for book business logic."""
    
    def __init__(self, db: Session):
        self.db = db
        self.crud = BookCRUD()
    
    def create_book(self, book_data: BookCreate) -> Dict[str, Any]:
        """
        Create a new book.
        
        Args:
            book_data: Book creation data
            
        Returns:
            Dict containing book ID and success message
            
        Raises:
            HTTPException: If creation fails
        """
        try:
            created_book = self.crud.create(self.db, book_data)
            return {
                "id": created_book.id,
                "message": "Book created successfully"
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def get_book_by_id(self, book_id: int) -> Dict[str, Any]:
        """
        Get a book by ID.
        
        Args:
            book_id: ID of the book to retrieve
            
        Returns:
            Dict containing book data
            
        Raises:
            HTTPException: If book not found
        """
        book = self.crud.get_by_id(self.db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "category": book.category,
            "price": float(book.price),
            "isbn": book.isbn
        }
    
    def get_all_books(self) -> List[Dict[str, Any]]:
        """
        Get all books.
        
        Returns:
            List of book dictionaries
        """
        books, _ = self.crud.get_multi(self.db, skip=0, limit=1000)
        
        return [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "price": float(book.price),
                "isbn": book.isbn
            }
            for book in books
        ]
    
    def update_book(self, book_id: int, book_data: BookUpdate) -> Dict[str, Any]:
        """
        Update a book.
        
        Args:
            book_id: ID of the book to update
            book_data: Book update data
            
        Returns:
            Dict containing success message
            
        Raises:
            HTTPException: If book not found
        """
        book = self.crud.update(self.db, book_id, book_data)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        return {
            "message": "Book updated successfully"
        }
    
    def delete_book(self, book_id: int) -> Dict[str, Any]:
        """
        Delete a book.
        
        Args:
            book_id: ID of the book to delete
            
        Returns:
            Dict containing success message
            
        Raises:
            HTTPException: If book not found
        """
        if not self.crud.delete(self.db, book_id):
            raise HTTPException(status_code=404, detail="Book not found")
        
        return {
            "message": "Book deleted successfully"
        }
    
    def search_books(self, query: str) -> List[Dict[str, Any]]:
        """
        Search books by title or author.
        
        Args:
            query: Search query
            
        Returns:
            List of matching books
        """
        books = self.crud.search(self.db, query)
        
        return [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "price": float(book.price),
                "isbn": book.isbn
            }
            for book in books
        ]
    
    def get_books_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get books by category.
        
        Args:
            category: Book category
            
        Returns:
            List of books in the category
        """
        books = self.crud.get_by_category(self.db, category)
        
        return [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "price": float(book.price),
                "isbn": book.isbn
            }
            for book in books
        ]
