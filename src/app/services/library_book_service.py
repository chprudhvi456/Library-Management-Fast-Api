"""
Library-Book Service Layer

This module contains the business logic for library-book mapping operations.
It acts as an intermediary between the API endpoints and the CRUD layer.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..crud.library_book import LibraryBookCRUD
from ..schemas.library_book import LibraryBookCreate, LibraryBookUpdate, LibraryBookResponse


class LibraryBookService:
    """Service class for library-book mapping business logic."""
    
    def __init__(self, db: Session):
        self.db = db
        self.crud = LibraryBookCRUD()
    
    def create_mapping(self, mapping_data: LibraryBookCreate) -> Dict[str, Any]:
        """
        Create a new library-book mapping.
        
        Args:
            mapping_data: Library-book mapping creation data
            
        Returns:
            Dict containing mapping ID and success message
            
        Raises:
            HTTPException: If creation fails
        """
        try:
            created_mapping = self.crud.create(self.db, mapping_data)
            return {
                "id": created_mapping.id,
                "message": "Library-book mapping created successfully"
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def get_mapping_by_id(self, mapping_id: int) -> Dict[str, Any]:
        """
        Get a library-book mapping by ID.
        
        Args:
            mapping_id: ID of the mapping to retrieve
            
        Returns:
            Dict containing mapping data
            
        Raises:
            HTTPException: If mapping not found
        """
        mapping = self.crud.get_by_id(self.db, mapping_id)
        if not mapping:
            raise HTTPException(status_code=404, detail="Library-book mapping not found")
        
        return {
            "id": mapping.id,
            "lib_id": mapping.lib_id,
            "book_id": mapping.book_id,
            "status": mapping.status
        }
    
    def get_all_mappings(self) -> List[Dict[str, Any]]:
        """
        Get all library-book mappings.
        
        Returns:
            List of mapping dictionaries
        """
        mappings, _ = self.crud.get_multi(self.db, skip=0, limit=1000)
        
        return [
            {
                "id": mapping.id,
                "lib_id": mapping.lib_id,
                "book_id": mapping.book_id,
                "status": mapping.status
            }
            for mapping in mappings
        ]
    
    def get_mappings_by_library(self, library_id: int) -> List[Dict[str, Any]]:
        """
        Get all mappings for a specific library.
        
        Args:
            library_id: ID of the library
            
        Returns:
            List of mappings for the library
        """
        mappings = self.crud.get_by_library(self.db, library_id)
        
        return [
            {
                "id": mapping.id,
                "lib_id": mapping.lib_id,
                "book_id": mapping.book_id,
                "status": mapping.status
            }
            for mapping in mappings
        ]
    
    def get_mappings_by_book(self, book_id: int) -> List[Dict[str, Any]]:
        """
        Get all mappings for a specific book.
        
        Args:
            book_id: ID of the book
            
        Returns:
            List of mappings for the book
        """
        mappings = self.crud.get_by_book(self.db, book_id)
        
        return [
            {
                "id": mapping.id,
                "lib_id": mapping.lib_id,
                "book_id": mapping.book_id,
                "status": mapping.status
            }
            for mapping in mappings
        ]
    
    def update_mapping(self, mapping_id: int, mapping_data: LibraryBookUpdate) -> Dict[str, Any]:
        """
        Update a library-book mapping.
        
        Args:
            mapping_id: ID of the mapping to update
            mapping_data: Mapping update data
            
        Returns:
            Dict containing success message
            
        Raises:
            HTTPException: If mapping not found
        """
        mapping = self.crud.update(self.db, mapping_id, mapping_data)
        if not mapping:
            raise HTTPException(status_code=404, detail="Library-book mapping not found")
        
        return {
            "message": "Library-book mapping updated successfully"
        }
    
    def delete_mapping(self, mapping_id: int) -> Dict[str, Any]:
        """
        Delete a library-book mapping.
        
        Args:
            mapping_id: ID of the mapping to delete
            
        Returns:
            Dict containing success message
            
        Raises:
            HTTPException: If mapping not found
        """
        if not self.crud.delete(self.db, mapping_id):
            raise HTTPException(status_code=404, detail="Library-book mapping not found")
        
        return {
            "message": "Library-book mapping deleted successfully"
        }
    
    def get_mapping_details(self, mapping_id: int) -> Dict[str, Any]:
        """
        Get detailed mapping information including library and book details.
        
        Args:
            mapping_id: ID of the mapping to retrieve
            
        Returns:
            Dict containing detailed mapping data
            
        Raises:
            HTTPException: If mapping not found
        """
        mapping = self.crud.get_with_details(self.db, mapping_id)
        if not mapping:
            raise HTTPException(status_code=404, detail="Library-book mapping not found")
        
        return {
            "id": mapping.id,
            "library": {
                "id": mapping.library.id,
                "name": mapping.library.name,
                "dept": mapping.library.dept,
                "status": mapping.library.status
            },
            "book": {
                "id": mapping.book.id,
                "title": mapping.book.title,
                "author": mapping.book.author,
                "isbn": mapping.book.isbn
            },
            "status": mapping.status
        }
