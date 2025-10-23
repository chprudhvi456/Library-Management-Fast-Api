from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class LibraryStatus(str, Enum):
    """Library status enumeration."""
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class LibraryBase(BaseModel):
    """Base library schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Library name")
    dept: Optional[str] = Field(None, max_length=100, description="Department")
    count: int = Field(0, ge=0, description="Number of books in library")
    status: LibraryStatus = Field(LibraryStatus.ACTIVE, description="Library status")


class LibraryCreate(LibraryBase):
    """Schema for creating a new library."""
    pass


class LibraryUpdate(BaseModel):
    """Schema for updating an existing library."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Library name")
    dept: Optional[str] = Field(None, max_length=100, description="Department")
    count: Optional[int] = Field(None, ge=0, description="Number of books in library")
    status: Optional[LibraryStatus] = Field(None, description="Library status")

    model_config = ConfigDict(extra="forbid")


class LibraryResponse(LibraryBase):
    """Schema for library response data."""
    id: int = Field(..., description="Library ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class LibraryListResponse(BaseModel):
    """Schema for paginated library list response."""
    libraries: List[LibraryResponse] = Field(..., description="List of libraries")
    total: int = Field(..., description="Total number of libraries")
    page: int = Field(..., ge=1, description="Current page number")
    size: int = Field(..., ge=1, description="Page size")
    pages: int = Field(..., ge=1, description="Total number of pages")

    model_config = ConfigDict(from_attributes=True)
