"""
Unit tests for model-schema mapping verification.
Tests that SQLAlchemy models correctly map to Pydantic schemas.
"""
import pytest
from datetime import datetime
from decimal import Decimal

from src.app.models.library import Library
from src.app.models.book import Book
from src.app.models.library_book import LibraryBook
from src.app.schemas.library import LibraryCreate, LibraryUpdate, LibraryResponse
from src.app.schemas.book import BookCreate, BookUpdate, BookResponse
from src.app.schemas.library_book import LibraryBookCreate, LibraryBookUpdate, LibraryBookResponse


class TestLibraryModelSchemaMapping:
    """Test Library model to schema mapping."""

    def test_library_create_schema(self):
        """Test LibraryCreate schema validation."""
        # Valid data
        valid_data = {
            "name": "Main Library",
            "dept": "CSE",
            "count": 200,
            "status": "Active"
        }
        library_create = LibraryCreate(**valid_data)
        assert library_create.name == "Main Library"
        assert library_create.dept == "CSE"
        assert library_create.count == 200
        assert library_create.status.value == "Active"

    def test_library_create_schema_minimal(self):
        """Test LibraryCreate schema with minimal required fields."""
        minimal_data = {
            "name": "Test Library"
        }
        library_create = LibraryCreate(**minimal_data)
        assert library_create.name == "Test Library"
        assert library_create.dept is None
        assert library_create.count == 0
        assert library_create.status.value == "Active"

    def test_library_update_schema(self):
        """Test LibraryUpdate schema validation."""
        update_data = {
            "name": "Updated Library",
            "status": "Inactive"
        }
        library_update = LibraryUpdate(**update_data)
        assert library_update.name == "Updated Library"
        assert library_update.status.value == "Inactive"
        assert library_update.dept is None
        assert library_update.count is None

    def test_library_response_schema(self):
        """Test LibraryResponse schema from model."""
        # Create a mock Library model instance
        library = Library()
        library.id = 1
        library.name = "Test Library"
        library.dept = "CSE"
        library.count = 100
        library.status = "Active"
        library.created_at = datetime.now()
        library.updated_at = datetime.now()

        # Convert to response schema
        library_response = LibraryResponse.model_validate(library)
        assert library_response.id == 1
        assert library_response.name == "Test Library"
        assert library_response.dept == "CSE"
        assert library_response.count == 100
        assert library_response.status.value == "Active"
        assert isinstance(library_response.created_at, datetime)
        assert isinstance(library_response.updated_at, datetime)

    def test_library_schema_validation_errors(self):
        """Test Library schema validation with invalid data."""
        # Test empty name
        with pytest.raises(ValueError):
            LibraryCreate(name="", dept="CSE")

        # Test negative count
        with pytest.raises(ValueError):
            LibraryCreate(name="Test", count=-1)

        # Test invalid status
        with pytest.raises(ValueError):
            LibraryCreate(name="Test", status="InvalidStatus")


class TestBookModelSchemaMapping:
    """Test Book model to schema mapping."""

    def test_book_create_schema(self):
        """Test BookCreate schema validation."""
        valid_data = {
            "title": "AI Fundamentals",
            "author": "John Smith",
            "category": "AI",
            "price": 550.00,
            "isbn": "9781234567890"
        }
        book_create = BookCreate(**valid_data)
        assert book_create.title == "AI Fundamentals"
        assert book_create.author == "John Smith"
        assert book_create.category == "AI"
        assert book_create.price == 550.00
        assert book_create.isbn == "9781234567890"

    def test_book_create_schema_minimal(self):
        """Test BookCreate schema with minimal required fields."""
        minimal_data = {
            "title": "Test Book",
            "author": "Test Author",
            "price": 100.0,
            "isbn": "1234567890"
        }
        book_create = BookCreate(**minimal_data)
        assert book_create.title == "Test Book"
        assert book_create.author == "Test Author"
        assert book_create.category is None
        assert book_create.price == 100.0
        assert book_create.isbn == "1234567890"

    def test_book_update_schema(self):
        """Test BookUpdate schema validation."""
        update_data = {
            "title": "Updated Book",
            "price": 600.0
        }
        book_update = BookUpdate(**update_data)
        assert book_update.title == "Updated Book"
        assert book_update.price == 600.0
        assert book_update.author is None
        assert book_update.category is None
        assert book_update.isbn is None

    def test_book_response_schema(self):
        """Test BookResponse schema from model."""
        # Create a mock Book model instance
        book = Book()
        book.id = 1
        book.title = "Test Book"
        book.author = "Test Author"
        book.category = "Test Category"
        book.price = Decimal("100.00")
        book.isbn = "1234567890"
        book.created_at = datetime.now()
        book.updated_at = datetime.now()

        # Convert to response schema
        book_response = BookResponse.model_validate(book)
        assert book_response.id == 1
        assert book_response.title == "Test Book"
        assert book_response.author == "Test Author"
        assert book_response.category == "Test Category"
        assert book_response.price == 100.0
        assert book_response.isbn == "1234567890"
        assert isinstance(book_response.created_at, datetime)
        assert isinstance(book_response.updated_at, datetime)

    def test_book_isbn_validation(self):
        """Test ISBN validation in Book schemas."""
        # Valid ISBNs
        valid_isbns = ["1234567890", "9781234567890", "978-1-234-56789-0"]
        for isbn in valid_isbns:
            book_data = {
                "title": "Test Book",
                "author": "Test Author",
                "price": 100.0,
                "isbn": isbn
            }
            book_create = BookCreate(**book_data)
            assert book_create.isbn == isbn

        # Invalid ISBNs
        invalid_isbns = ["123", "abc123", "12345678901234567890"]
        for isbn in invalid_isbns:
            with pytest.raises(ValueError):
                BookCreate(
                    title="Test Book",
                    author="Test Author",
                    price=100.0,
                    isbn=isbn
                )

    def test_book_schema_validation_errors(self):
        """Test Book schema validation with invalid data."""
        # Test empty title
        with pytest.raises(ValueError):
            BookCreate(title="", author="Author", price=100.0, isbn="1234567890")

        # Test negative price
        with pytest.raises(ValueError):
            BookCreate(title="Test", author="Author", price=-100.0, isbn="1234567890")


class TestLibraryBookModelSchemaMapping:
    """Test LibraryBook model to schema mapping."""

    def test_library_book_create_schema(self):
        """Test LibraryBookCreate schema validation."""
        valid_data = {
            "lib_id": 1,
            "book_id": 1,
            "status": "Active"
        }
        library_book_create = LibraryBookCreate(**valid_data)
        assert library_book_create.lib_id == 1
        assert library_book_create.book_id == 1
        assert library_book_create.status.value == "Active"

    def test_library_book_create_schema_minimal(self):
        """Test LibraryBookCreate schema with minimal required fields."""
        minimal_data = {
            "lib_id": 1,
            "book_id": 1
        }
        library_book_create = LibraryBookCreate(**minimal_data)
        assert library_book_create.lib_id == 1
        assert library_book_create.book_id == 1
        assert library_book_create.status.value == "Active"

    def test_library_book_update_schema(self):
        """Test LibraryBookUpdate schema validation."""
        update_data = {
            "status": "Inactive"
        }
        library_book_update = LibraryBookUpdate(**update_data)
        assert library_book_update.status.value == "Inactive"
        assert library_book_update.lib_id is None
        assert library_book_update.book_id is None

    def test_library_book_response_schema(self):
        """Test LibraryBookResponse schema from model."""
        # Create a mock LibraryBook model instance
        library_book = LibraryBook()
        library_book.id = 1
        library_book.lib_id = 1
        library_book.book_id = 1
        library_book.status = "Active"
        library_book.created_at = datetime.now()
        library_book.updated_at = datetime.now()

        # Convert to response schema
        library_book_response = LibraryBookResponse.model_validate(library_book)
        assert library_book_response.id == 1
        assert library_book_response.lib_id == 1
        assert library_book_response.book_id == 1
        assert library_book_response.status.value == "Active"
        assert isinstance(library_book_response.created_at, datetime)
        assert isinstance(library_book_response.updated_at, datetime)

    def test_library_book_schema_validation_errors(self):
        """Test LibraryBook schema validation with invalid data."""
        # Test negative lib_id
        with pytest.raises(ValueError):
            LibraryBookCreate(lib_id=-1, book_id=1)

        # Test negative book_id
        with pytest.raises(ValueError):
            LibraryBookCreate(lib_id=1, book_id=-1)

        # Test invalid status
        with pytest.raises(ValueError):
            LibraryBookCreate(lib_id=1, book_id=1, status="InvalidStatus")


class TestSchemaFieldMapping:
    """Test that all model fields are correctly mapped to schemas."""

    def test_library_model_fields_mapped(self):
        """Test that all Library model fields are mapped in schemas."""
        # Check that all Library model fields are present in response schema
        library_fields = ['id', 'name', 'dept', 'count', 'status', 'created_at', 'updated_at']
        response_fields = LibraryResponse.model_fields.keys()
        
        for field in library_fields:
            assert field in response_fields, f"Field {field} not found in LibraryResponse"

    def test_book_model_fields_mapped(self):
        """Test that all Book model fields are mapped in schemas."""
        # Check that all Book model fields are present in response schema
        book_fields = ['id', 'title', 'author', 'category', 'price', 'isbn', 'created_at', 'updated_at']
        response_fields = BookResponse.model_fields.keys()
        
        for field in book_fields:
            assert field in response_fields, f"Field {field} not found in BookResponse"

    def test_library_book_model_fields_mapped(self):
        """Test that all LibraryBook model fields are mapped in schemas."""
        # Check that all LibraryBook model fields are present in response schema
        library_book_fields = ['id', 'lib_id', 'book_id', 'status', 'created_at', 'updated_at']
        response_fields = LibraryBookResponse.model_fields.keys()
        
        for field in library_book_fields:
            assert field in response_fields, f"Field {field} not found in LibraryBookResponse"
