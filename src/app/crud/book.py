from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Tuple
from ..models.book import Book
from ..schemas.book import BookCreate, BookUpdate


class BookCRUD:
    """CRUD operations for Book model."""

    @staticmethod
    def create(db: Session, book: BookCreate) -> Book:
        """Create a new book."""
        db_book = Book(
            title=book.title,
            author=book.author,
            category=book.category,
            price=book.price,
            isbn=book.isbn
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def get_by_id(db: Session, book_id: int) -> Optional[Book]:
        """Get a book by ID."""
        return db.query(Book).filter(Book.id == book_id).first()

    @staticmethod
    def get_by_isbn(db: Session, isbn: str) -> Optional[Book]:
        """Get a book by ISBN."""
        return db.query(Book).filter(Book.isbn == isbn).first()

    @staticmethod
    def get_multi(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> Tuple[List[Book], int]:
        """Get multiple books with optional filtering and pagination."""
        query = db.query(Book)
        
        # Apply filters
        if search:
            query = query.filter(
                or_(
                    Book.title.ilike(f"%{search}%"),
                    Book.author.ilike(f"%{search}%"),
                    Book.category.ilike(f"%{search}%")
                )
            )
        
        if category:
            query = query.filter(Book.category == category)
            
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        
        if min_price is not None:
            query = query.filter(Book.price >= min_price)
            
        if max_price is not None:
            query = query.filter(Book.price <= max_price)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        books = query.offset(skip).limit(limit).all()
        
        return books, total

    @staticmethod
    def update(db: Session, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        """Update a book."""
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            return None
        
        update_data = book_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_book, field, value)
        
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def delete(db: Session, book_id: int) -> bool:
        """Delete a book."""
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            return False
        
        db.delete(db_book)
        db.commit()
        return True

    @staticmethod
    def get_by_category(db: Session, category: str) -> List[Book]:
        """Get all books in a specific category."""
        return db.query(Book).filter(Book.category == category).all()

    @staticmethod
    def get_by_author(db: Session, author: str) -> List[Book]:
        """Get all books by a specific author."""
        return db.query(Book).filter(Book.author.ilike(f"%{author}%")).all()

    @staticmethod
    def search_by_title(db: Session, title: str) -> List[Book]:
        """Search books by title (case-insensitive partial match)."""
        return db.query(Book).filter(Book.title.ilike(f"%{title}%")).all()

    @staticmethod
    def get_price_range(db: Session, min_price: float, max_price: float) -> List[Book]:
        """Get books within a specific price range."""
        return db.query(Book).filter(
            and_(
                Book.price >= min_price,
                Book.price <= max_price
            )
        ).all()

    @staticmethod
    def get_categories(db: Session) -> List[str]:
        """Get all unique categories."""
        categories = db.query(Book.category).filter(Book.category.isnot(None)).distinct().all()
        return [cat[0] for cat in categories if cat[0]]

    @staticmethod
    def get_authors(db: Session) -> List[str]:
        """Get all unique authors."""
        authors = db.query(Book.author).distinct().all()
        return [author[0] for author in authors]
