from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class LibraryBook(Base):
    """
    LibraryBook model representing the many-to-many relationship between libraries and books.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        lib_id: Foreign key to libraries.id (required)
        book_id: Foreign key to books.id (required)
        status: Mapping status - Active or Inactive (default Active)
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    __tablename__ = "library_books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lib_id = Column(Integer, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(
        Enum('Active', 'Inactive', name='mapping_status'),
        nullable=False,
        default='Active',
        index=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    library = relationship("Library", back_populates="library_books")
    book = relationship("Book", back_populates="library_books")

    # Unique constraint to prevent duplicate library-book mappings
    __table_args__ = (
        UniqueConstraint('lib_id', 'book_id', name='unique_library_book'),
    )

    def __repr__(self):
        return f"<LibraryBook(id={self.id}, lib_id={self.lib_id}, book_id={self.book_id}, status='{self.status}')>"
