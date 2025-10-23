from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Library(Base):
    """
    Library model representing a library entity.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        name: Library name (required, max 255 characters)
        dept: Department (optional, max 100 characters)
        count: Number of books in library (default 0)
        status: Library status - Active or Inactive (default Active)
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    dept = Column(String(100), nullable=True, index=True)
    count = Column(Integer, default=0, nullable=False)
    status = Column(
        Enum('Active', 'Inactive', name='library_status'),
        nullable=False,
        default='Active',
        index=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    library_books = relationship("LibraryBook", back_populates="library", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Library(id={self.id}, name='{self.name}', dept='{self.dept}', status='{self.status}')>"
