"""
Library Service Layer

This module contains the business logic for library operations.
It acts as an intermediary between the API endpoints and the CRUD layer.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..crud.library import LibraryCRUD
from ..crud.library_book import LibraryBookCRUD
from ..schemas.library import LibraryCreate, LibraryUpdate, LibraryResponse


class LibraryService:
    """Service class for library business logic."""
    
    def __init__(self, db: Session):
        self.db = db
        self.crud = LibraryCRUD()
        self.library_book_crud = LibraryBookCRUD()
    
    def create_library(self, library_data: LibraryCreate) -> Dict[str, Any]:
        """
        Create a new library.
        
        Args:
            library_data: Library creation data
            
        Returns:
            Dict containing library ID and success message
            
        Raises:
            HTTPException: If creation fails
        """
        try:
            created_library = self.crud.create(self.db, library_data)
            return {
                "id": created_library.id,
                "message": "Library created successfully"
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def get_library_by_id(self, library_id: int) -> Dict[str, Any]:
        """
        Get a library by ID.
        
        Args:
            library_id: ID of the library to retrieve
            
        Returns:
            Dict containing library data
            
        Raises:
            HTTPException: If library not found
        """
        library = self.crud.get_by_id(self.db, library_id)
        if not library:
            raise HTTPException(status_code=404, detail="Library not found")
        
        return {
            "id": library.id,
            "name": library.name,
            "dept": library.dept,
            "count": library.count,
            "status": library.status
        }
    
    def get_all_libraries(self) -> List[Dict[str, Any]]:
        """
        Get all libraries.
        
        Returns:
            List of library dictionaries
        """
        libraries, _ = self.crud.get_multi(self.db, skip=0, limit=1000)
        
        return [
            {
                "id": lib.id,
                "name": lib.name,
                "dept": lib.dept,
                "count": lib.count,
                "status": lib.status
            }
            for lib in libraries
        ]
    
    def update_library(self, library_id: int, library_data: LibraryUpdate) -> Dict[str, Any]:
        """
        Update a library.
        
        Args:
            library_id: ID of the library to update
            library_data: Library update data
            
        Returns:
            Dict containing success message
            
        Raises:
            HTTPException: If library not found
        """
        library = self.crud.update(self.db, library_id, library_data)
        if not library:
            raise HTTPException(status_code=404, detail="Library not found")
        
        return {
            "message": "Library updated successfully"
        }
    
    def delete_library(self, library_id: int) -> Dict[str, Any]:
        """
        Delete a library.
        
        Args:
            library_id: ID of the library to delete
            
        Returns:
            Dict containing success message
            
        Raises:
            HTTPException: If library not found
        """
        if not self.crud.delete(self.db, library_id):
            raise HTTPException(status_code=404, detail="Library not found")
        
        return {
            "message": "Library deleted successfully"
        }
    
    def get_library_stats(self) -> Dict[str, Any]:
        """
        Get library statistics.
        
        Returns:
            Dict containing library statistics
        """
        libraries, total = self.crud.get_multi(self.db, skip=0, limit=1000)
        
        active_libraries = sum(1 for lib in libraries if lib.status == "Active")
        inactive_libraries = total - active_libraries
        
        return {
            "total_libraries": total,
            "active_libraries": active_libraries,
            "inactive_libraries": inactive_libraries
        }
    
    def get_library_books(self, library_id: int, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all books in a specific library with joined metadata.
        
        Args:
            library_id: ID of the library
            status: Optional status filter (Active/Inactive)
            
        Returns:
            List of book dictionaries with joined metadata
            
        Raises:
            HTTPException: If library not found
        """
        # First check if library exists
        library = self.crud.get_by_id(self.db, library_id)
        if not library:
            raise HTTPException(status_code=404, detail="Library not found")
        
        # Get books in library with efficient JOIN query
        mappings = self.library_book_crud.get_books_in_library(self.db, library_id, status)
        
        # Format response with joined book metadata
        books = []
        for mapping in mappings:
            book = mapping.book  # This is loaded via joinedload
            books.append({
                "book_id": book.id,
                "title": book.title,
                "status": mapping.status,
                "author": book.author,
                "category": book.category,
                "isbn": book.isbn
            })
        
        return books
