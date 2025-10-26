from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Tuple
from ..models.library import Library
from ..schemas.library import LibraryCreate, LibraryUpdate


class LibraryCRUD:
    """CRUD operations for Library model."""

    @staticmethod
    def create(db: Session, library: LibraryCreate) -> Library:
        """Create a new library."""
        db_library = Library(
            name=library.name,
            dept=library.dept,
            count=library.count,
            status=library.status.value
        )
        db.add(db_library)
        db.commit()
        db.refresh(db_library)
        return db_library

    @staticmethod
    def get_by_id(db: Session, library_id: int) -> Optional[Library]:
        """Get a library by ID."""
        return db.query(Library).filter(Library.id == library_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Library]:
        """Get a library by name."""
        return db.query(Library).filter(Library.name == name).first()

    @staticmethod
    def get_multi(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        status: Optional[str] = None,
        dept: Optional[str] = None
    ) -> Tuple[List[Library], int]:
        """Get multiple libraries with optional filtering and pagination."""
        query = db.query(Library)
        
        # Apply filters
        if search:
            query = query.filter(
                or_(
                    Library.name.ilike(f"%{search}%"),
                    Library.dept.ilike(f"%{search}%")
                )
            )
        
        if status:
            query = query.filter(Library.status == status)
            
        if dept:
            query = query.filter(Library.dept == dept)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        libraries = query.offset(skip).limit(limit).all()
        
        return libraries, total

    @staticmethod
    def update(db: Session, library_id: int, library_update: LibraryUpdate) -> Optional[Library]:
        """Update a library."""
        db_library = db.query(Library).filter(Library.id == library_id).first()
        if not db_library:
            return None
        
        update_data = library_update.model_dump(exclude_unset=True)
        if 'status' in update_data and update_data['status']:
            update_data['status'] = update_data['status'].value
        
        for field, value in update_data.items():
            setattr(db_library, field, value)
        
        db.commit()
        db.refresh(db_library)
        return db_library

    @staticmethod
    def delete(db: Session, library_id: int) -> bool:
        """Delete a library."""
        db_library = db.query(Library).filter(Library.id == library_id).first()
        if not db_library:
            return False
        
        db.delete(db_library)
        db.commit()
        return True

    @staticmethod
    def update_book_count(db: Session, library_id: int) -> Optional[Library]:
        """Update the book count for a library based on active mappings."""
        db_library = db.query(Library).filter(Library.id == library_id).first()
        if not db_library:
            return None
        
        # Count active library-book mappings
        from ..models.library_book import LibraryBook
        count = db.query(LibraryBook).filter(
            and_(
                LibraryBook.lib_id == library_id,
                LibraryBook.status == 'Active'
            )
        ).count()
        
        db_library.count = count
        db.commit()
        db.refresh(db_library)
        return db_library

    @staticmethod
    def get_by_department(db: Session, dept: str) -> List[Library]:
        """Get all libraries in a specific department."""
        return db.query(Library).filter(Library.dept == dept).all()

    @staticmethod
    def get_active_libraries(db: Session) -> List[Library]:
        """Get all active libraries."""
        return db.query(Library).filter(Library.status == 'Active').all()
    
    @staticmethod
    def increment_count(db: Session, library_id: int) -> Optional[Library]:
        """Increment the book count for a library."""
        db_library = db.query(Library).filter(Library.id == library_id).first()
        if not db_library:
            return None
        
        db_library.count += 1
        db.commit()
        db.refresh(db_library)
        return db_library
    
    @staticmethod
    def decrement_count(db: Session, library_id: int) -> Optional[Library]:
        """Decrement the book count for a library."""
        db_library = db.query(Library).filter(Library.id == library_id).first()
        if not db_library:
            return None
        
        # Ensure count doesn't go below 0
        if db_library.count > 0:
            db_library.count -= 1
            db.commit()
            db.refresh(db_library)
        
        return db_library
