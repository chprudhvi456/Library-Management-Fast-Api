from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
import re


class BookBase(BaseModel):
    """Base book schema with common fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Book title")
    author: str = Field(..., min_length=1, max_length=255, description="Book author")
    category: Optional[str] = Field(None, max_length=100, description="Book category")
    price: float = Field(..., gt=0, description="Book price")
    isbn: str = Field(..., min_length=10, max_length=20, description="International Standard Book Number")

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v):
        """Validate ISBN format (basic validation)."""
        # Remove any hyphens or spaces
        isbn_clean = re.sub(r'[-\s]', '', v)
        # Check if it's numeric and has valid length
        if not isbn_clean.isdigit():
            raise ValueError('ISBN must contain only digits, hyphens, and spaces')
        if len(isbn_clean) not in [10, 13]:
            raise ValueError('ISBN must be 10 or 13 digits long')
        return v


class BookCreate(BookBase):
    """Schema for creating a new book."""
    pass


class BookUpdate(BaseModel):
    """Schema for updating an existing book."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Book title")
    author: Optional[str] = Field(None, min_length=1, max_length=255, description="Book author")
    category: Optional[str] = Field(None, max_length=100, description="Book category")
    price: Optional[float] = Field(None, gt=0, description="Book price")
    isbn: Optional[str] = Field(None, min_length=10, max_length=20, description="International Standard Book Number")

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v):
        """Validate ISBN format (basic validation)."""
        if v is not None:
            # Remove any hyphens or spaces
            isbn_clean = re.sub(r'[-\s]', '', v)
            # Check if it's numeric and has valid length
            if not isbn_clean.isdigit():
                raise ValueError('ISBN must contain only digits, hyphens, and spaces')
            if len(isbn_clean) not in [10, 13]:
                raise ValueError('ISBN must be 10 or 13 digits long')
        return v

    model_config = ConfigDict(extra="forbid")


class BookResponse(BookBase):
    """Schema for book response data."""
    id: int = Field(..., description="Book ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class BookListResponse(BaseModel):
    """Schema for paginated book list response."""
    books: List[BookResponse] = Field(..., description="List of books")
    total: int = Field(..., description="Total number of books")
    page: int = Field(..., ge=1, description="Current page number")
    size: int = Field(..., ge=1, description="Page size")
    pages: int = Field(..., ge=1, description="Total number of pages")

    model_config = ConfigDict(from_attributes=True)
