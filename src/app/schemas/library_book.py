from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MappingStatus(str, Enum):
    """Library-Book mapping status enumeration."""
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class LibraryBookBase(BaseModel):
    """Base library-book mapping schema with common fields."""
    lib_id: int = Field(..., gt=0, description="Library ID")
    book_id: int = Field(..., gt=0, description="Book ID")
    status: MappingStatus = Field(MappingStatus.ACTIVE, description="Mapping status")


class LibraryBookCreate(LibraryBookBase):
    """Schema for creating a new library-book mapping."""
    pass


class LibraryBookUpdate(BaseModel):
    """Schema for updating an existing library-book mapping."""
    lib_id: Optional[int] = Field(None, gt=0, description="Library ID")
    book_id: Optional[int] = Field(None, gt=0, description="Book ID")
    status: Optional[MappingStatus] = Field(None, description="Mapping status")

    model_config = ConfigDict(extra="forbid")


class LibraryBookResponse(LibraryBookBase):
    """Schema for library-book mapping response data."""
    id: int = Field(..., description="Mapping ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class LibraryBookWithDetailsResponse(LibraryBookResponse):
    """Schema for library-book mapping with related entity details."""
    library_name: Optional[str] = Field(None, description="Library name")
    book_title: Optional[str] = Field(None, description="Book title")
    book_author: Optional[str] = Field(None, description="Book author")

    model_config = ConfigDict(from_attributes=True)


class LibraryBookListResponse(BaseModel):
    """Schema for paginated library-book mapping list response."""
    mappings: List[LibraryBookWithDetailsResponse] = Field(..., description="List of library-book mappings")
    total: int = Field(..., description="Total number of mappings")
    page: int = Field(..., ge=1, description="Current page number")
    size: int = Field(..., ge=1, description="Page size")
    pages: int = Field(..., ge=1, description="Total number of pages")

    model_config = ConfigDict(from_attributes=True)
