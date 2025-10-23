from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import List, Optional, Tuple
from ..models.library_book import LibraryBook
from ..models.library import Library
from ..models.book import Book
from ..schemas.library_book import LibraryBookCreate, LibraryBookUpdate


class LibraryBookCRUD:
    """CRUD operations for LibraryBook model."""

    @staticmethod
    def create(db: Session, library_book: LibraryBookCreate) -> LibraryBook:
        """Create a new library-book mapping."""
        db_library_book = LibraryBook(
            lib_id=library_book.lib_id,
            book_id=library_book.book_id,
            status=library_book.status.value
        )
        db.add(db_library_book)
        db.commit()
        db.refresh(db_library_book)
        return db_library_book

    @staticmethod
    def get_by_id(db: Session, mapping_id: int) -> Optional[LibraryBook]:
        """Get a library-book mapping by ID."""
        return db.query(LibraryBook).filter(LibraryBook.id == mapping_id).first()

    @staticmethod
    def get_by_library_and_book(db: Session, lib_id: int, book_id: int) -> Optional[LibraryBook]:
        """Get a library-book mapping by library ID and book ID."""
        return db.query(LibraryBook).filter(
            and_(
                LibraryBook.lib_id == lib_id,
                LibraryBook.book_id == book_id
            )
        ).first()

    @staticmethod
    def get_multi(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        lib_id: Optional[int] = None,
        book_id: Optional[int] = None,
        status: Optional[str] = None,
        include_details: bool = False
    ) -> Tuple[List[LibraryBook], int]:
        """Get multiple library-book mappings with optional filtering and pagination."""
        query = db.query(LibraryBook)
        
        # Apply filters
        if lib_id:
            query = query.filter(LibraryBook.lib_id == lib_id)
            
        if book_id:
            query = query.filter(LibraryBook.book_id == book_id)
            
        if status:
            query = query.filter(LibraryBook.status == status)
        
        # Include related entity details if requested
        if include_details:
            query = query.options(
                joinedload(LibraryBook.library),
                joinedload(LibraryBook.book)
            )
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        mappings = query.offset(skip).limit(limit).all()
        
        return mappings, total

    @staticmethod
    def update(db: Session, mapping_id: int, mapping_update: LibraryBookUpdate) -> Optional[LibraryBook]:
        """Update a library-book mapping."""
        db_mapping = db.query(LibraryBook).filter(LibraryBook.id == mapping_id).first()
        if not db_mapping:
            return None
        
        update_data = mapping_update.model_dump(exclude_unset=True)
        if 'status' in update_data and update_data['status']:
            update_data['status'] = update_data['status'].value
        
        for field, value in update_data.items():
            setattr(db_mapping, field, value)
        
        db.commit()
        db.refresh(db_mapping)
        return db_mapping

    @staticmethod
    def delete(db: Session, mapping_id: int) -> bool:
        """Delete a library-book mapping."""
        db_mapping = db.query(LibraryBook).filter(LibraryBook.id == mapping_id).first()
        if not db_mapping:
            return False
        
        db.delete(db_mapping)
        db.commit()
        return True

    @staticmethod
    def delete_by_library_and_book(db: Session, lib_id: int, book_id: int) -> bool:
        """Delete a library-book mapping by library ID and book ID."""
        db_mapping = db.query(LibraryBook).filter(
            and_(
                LibraryBook.lib_id == lib_id,
                LibraryBook.book_id == book_id
            )
        ).first()
        if not db_mapping:
            return False
        
        db.delete(db_mapping)
        db.commit()
        return True

    @staticmethod
    def get_books_in_library(db: Session, lib_id: int, status: Optional[str] = None) -> List[LibraryBook]:
        """Get all books in a specific library."""
        query = db.query(LibraryBook).filter(LibraryBook.lib_id == lib_id)
        
        if status:
            query = query.filter(LibraryBook.status == status)
        
        return query.options(joinedload(LibraryBook.book)).all()

    @staticmethod
    def get_libraries_for_book(db: Session, book_id: int, status: Optional[str] = None) -> List[LibraryBook]:
        """Get all libraries that have a specific book."""
        query = db.query(LibraryBook).filter(LibraryBook.book_id == book_id)
        
        if status:
            query = query.filter(LibraryBook.status == status)
        
        return query.options(joinedload(LibraryBook.library)).all()

    @staticmethod
    def get_active_mappings(db: Session) -> List[LibraryBook]:
        """Get all active library-book mappings."""
        return db.query(LibraryBook).filter(LibraryBook.status == 'Active').all()

    @staticmethod
    def get_mappings_by_status(db: Session, status: str) -> List[LibraryBook]:
        """Get all library-book mappings with a specific status."""
        return db.query(LibraryBook).filter(LibraryBook.status == status).all()

    @staticmethod
    def count_books_in_library(db: Session, lib_id: int, status: Optional[str] = None) -> int:
        """Count books in a specific library."""
        query = db.query(LibraryBook).filter(LibraryBook.lib_id == lib_id)
        
        if status:
            query = query.filter(LibraryBook.status == status)
        
        return query.count()

    @staticmethod
    def count_libraries_for_book(db: Session, book_id: int, status: Optional[str] = None) -> int:
        """Count libraries that have a specific book."""
        query = db.query(LibraryBook).filter(LibraryBook.book_id == book_id)
        
        if status:
            query = query.filter(LibraryBook.status == status)
        
        return query.count()

    @staticmethod
    def exists(db: Session, lib_id: int, book_id: int) -> bool:
        """Check if a library-book mapping exists."""
        return db.query(LibraryBook).filter(
            and_(
                LibraryBook.lib_id == lib_id,
                LibraryBook.book_id == book_id
            )
        ).first() is not None
