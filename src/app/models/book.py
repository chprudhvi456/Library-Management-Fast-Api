from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Book(Base):
    """
    Book model representing a book entity.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        title: Book title (required, max 255 characters)
        author: Book author (required, max 255 characters)
        category: Book category (optional, max 100 characters)
        price: Book price (required, decimal with 2 decimal places)
        isbn: International Standard Book Number (required, unique, max 20 characters)
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    isbn = Column(String(20), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    library_books = relationship("LibraryBook", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', isbn='{self.isbn}')>"
