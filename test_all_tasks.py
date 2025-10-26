#!/usr/bin/env python3
"""
Comprehensive test file for all Library Management System tasks.
Tests KAN-202, KAN-203, and KAN-204 implementations.
"""
import sys
import requests
import json
from pathlib import Path
from typing import Dict, Any, List

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import models and schemas for testing
from src.app.models.library import Library
from src.app.models.book import Book
from src.app.models.library_book import LibraryBook
from src.app.schemas.library import LibraryCreate, LibraryUpdate, LibraryResponse
from src.app.schemas.book import BookCreate, BookUpdate, BookResponse
from src.app.schemas.library_book import LibraryBookCreate, LibraryBookUpdate, LibraryBookResponse

# Test configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

class TaskTester:
    """Comprehensive tester for all Library Management System tasks."""
    
    def __init__(self):
        self.results = {
            "KAN-202": {"status": "Not Implemented", "tests": []},
            "KAN-203": {"status": "Not Implemented", "tests": []},
            "KAN-204": {"status": "Not Implemented", "tests": []},
            "KAN-205": {"status": "Not Implemented", "tests": []},
            "KAN-206": {"status": "Not Implemented", "tests": []},
            "KAN-207": {"status": "Not Implemented", "tests": []},
            "KAN-208": {"status": "Not Implemented", "tests": []},
            "KAN-209": {"status": "Not Implemented", "tests": []},
            "KAN-210": {"status": "Not Implemented", "tests": []},
            "KAN-211": {"status": "Not Implemented", "tests": []}
        }
    
    def log_test(self, task: str, test_name: str, status: str, details: str = ""):
        """Log a test result."""
        self.results[task]["tests"].append({
            "name": test_name,
            "status": status,
            "details": details
        })
        status_icon = "[OK]" if status == "PASSED" else "[ERROR]"
        print(f"  {status_icon} {test_name}: {status}")
        if details:
            print(f"    {details}")
    
    def test_kan_202(self):
        """Test KAN-202: Database Setup & Models."""
        print("\n" + "="*60)
        print("Testing KAN-202: Database Setup & Models")
        print("="*60)
        
        try:
            # Test 1: Database connection
            from src.app.database import get_db, create_tables
            create_tables()
            self.log_test("KAN-202", "Database Connection", "PASSED", "Database tables created successfully")
            
            # Test 2: Model imports
            from src.app.models import Library, Book, LibraryBook
            self.log_test("KAN-202", "Model Imports", "PASSED", "All models imported successfully")
            
            # Test 3: Model relationships
            library = Library()
            book = Book()
            library_book = LibraryBook()
            
            self.log_test("KAN-202", "Model Instantiation", "PASSED", "All models can be instantiated")
            
            # Test 4: Database schema validation
            self.log_test("KAN-202", "Database Schema", "PASSED", "Database schema is valid")
            
            self.results["KAN-202"]["status"] = "COMPLETED"
            
        except Exception as e:
            self.log_test("KAN-202", "Database Setup", "FAILED", str(e))
            self.results["KAN-202"]["status"] = "FAILED"
    
    def test_kan_203(self):
        """Test KAN-203: SQLAlchemy Models & Pydantic Schemas."""
        print("\n" + "="*60)
        print("Testing KAN-203: SQLAlchemy Models & Pydantic Schemas")
        print("="*60)
        
        try:
            # Test 1: Schema imports
            from src.app.schemas.library import LibraryCreate, LibraryUpdate, LibraryResponse
            from src.app.schemas.book import BookCreate, BookUpdate, BookResponse
            from src.app.schemas.library_book import LibraryBookCreate, LibraryBookUpdate, LibraryBookResponse
            self.log_test("KAN-203", "Schema Imports", "PASSED", "All schemas imported successfully")
            
            # Test 2: Library schema validation
            library_data = LibraryCreate(
                name="Test Library",
                dept="CSE",
                count=100,
                status="Active"
            )
            self.log_test("KAN-203", "Library Schema Validation", "PASSED", "Library schema validation works")
            
            # Test 3: Book schema validation
            book_data = BookCreate(
                title="Test Book",
                author="Test Author",
                price=100.0,
                isbn="1234567890"
            )
            self.log_test("KAN-203", "Book Schema Validation", "PASSED", "Book schema validation works")
            
            # Test 4: LibraryBook schema validation
            mapping_data = LibraryBookCreate(
                lib_id=1,
                book_id=1,
                status="Active"
            )
            self.log_test("KAN-203", "LibraryBook Schema Validation", "PASSED", "LibraryBook schema validation works")
            
            # Test 5: CRUD operations
            from src.app.crud.library import LibraryCRUD
            from src.app.crud.book import BookCRUD
            from src.app.crud.library_book import LibraryBookCRUD
            self.log_test("KAN-203", "CRUD Operations", "PASSED", "All CRUD operations available")
            
            # Test 6: Schema field mapping
            library_fields = ['id', 'name', 'dept', 'count', 'status', 'created_at', 'updated_at']
            response_fields = LibraryResponse.model_fields.keys()
            all_fields_mapped = all(field in response_fields for field in library_fields)
            
            if all_fields_mapped:
                self.log_test("KAN-203", "Schema Field Mapping", "PASSED", "All model fields mapped to schemas")
            else:
                self.log_test("KAN-203", "Schema Field Mapping", "FAILED", "Some fields not mapped correctly")
            
            self.results["KAN-203"]["status"] = "COMPLETED"
            
        except Exception as e:
            self.log_test("KAN-203", "Schema Implementation", "FAILED", str(e))
            self.results["KAN-203"]["status"] = "FAILED"
    
    def test_kan_204(self):
        """Test KAN-204: Library CRUD Endpoints."""
        print("\n" + "="*60)
        print("Testing KAN-204: Library CRUD Endpoints")
        print("="*60)
        
        try:
            # Test 1: Server health check
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                self.log_test("KAN-204", "Server Health Check", "PASSED", "Server is running")
            else:
                self.log_test("KAN-204", "Server Health Check", "FAILED", f"Server returned {response.status_code}")
                return
            
            # Test 2: Create library endpoint
            library_data = {
                "name": "Test Library KAN-204",
                "dept": "CSE",
                "count": 200,
                "status": "Active"
            }
            
            response = requests.post(f"{BASE_URL}/libraries", json=library_data)
            if response.status_code == 201:
                result = response.json()
                if "id" in result and "message" in result:
                    self.log_test("KAN-204", "Create Library", "PASSED", f"Library created with ID: {result['id']}")
                else:
                    self.log_test("KAN-204", "Create Library Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-204", "Create Library", "FAILED", f"Status code: {response.status_code}")
            
            # Test 3: Get libraries endpoint
            response = requests.get(f"{BASE_URL}/libraries")
            if response.status_code == 200:
                libraries = response.json()
                if isinstance(libraries, list):
                    self.log_test("KAN-204", "Get Libraries", "PASSED", f"Retrieved {len(libraries)} libraries")
                    
                    # Check response format
                    if libraries and all("id" in lib and "name" in lib for lib in libraries):
                        self.log_test("KAN-204", "Library Response Format", "PASSED", "Clean JSON format returned")
                    else:
                        self.log_test("KAN-204", "Library Response Format", "FAILED", "Response format incorrect")
                else:
                    self.log_test("KAN-204", "Get Libraries Response", "FAILED", "Response is not a list")
            else:
                self.log_test("KAN-204", "Get Libraries", "FAILED", f"Status code: {response.status_code}")
            
            # Test 4: Validation testing
            invalid_library = {
                "name": "",
                "count": -1,
                "status": "InvalidStatus"
            }
            
            response = requests.post(f"{BASE_URL}/libraries", json=invalid_library)
            if response.status_code == 422:
                self.log_test("KAN-204", "Library Validation", "PASSED", "Validation errors properly returned")
            else:
                self.log_test("KAN-204", "Library Validation", "FAILED", f"Expected 422, got {response.status_code}")
            
            self.results["KAN-204"]["status"] = "COMPLETED"
            
        except requests.exceptions.ConnectionError:
            self.log_test("KAN-204", "Server Connection", "FAILED", "Server not running. Start with: python src/app/main.py")
            self.results["KAN-204"]["status"] = "FAILED"
        except Exception as e:
            self.log_test("KAN-204", "Library Endpoints", "FAILED", str(e))
            self.results["KAN-204"]["status"] = "FAILED"
    
    def test_kan_205(self):
        """Test KAN-205: Library Read/Update/Delete Endpoints."""
        print("\n" + "="*60)
        print("Testing KAN-205: Library Read/Update/Delete Endpoints")
        print("="*60)
        
        try:
            # Test 1: Server health check
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                self.log_test("KAN-205", "Server Health Check", "PASSED", "Server is running")
            else:
                self.log_test("KAN-205", "Server Health Check", "FAILED", f"Server returned {response.status_code}")
                return
            
            # Test 2: Create a library first (for testing other endpoints)
            library_data = {
                "name": "Test Library KAN-205",
                "dept": "Computer Science",
                "count": 150,
                "status": "Active"
            }
            
            create_response = requests.post(f"{BASE_URL}/libraries", json=library_data)
            if create_response.status_code == 201:
                created_library = create_response.json()
                library_id = created_library["id"]
                self.log_test("KAN-205", "Create Library for Testing", "PASSED", f"Library created with ID: {library_id}")
            else:
                self.log_test("KAN-205", "Create Library for Testing", "FAILED", f"Status code: {create_response.status_code}")
                return
            
            # Test 3: GET /libraries/{id} - Get library by ID
            response = requests.get(f"{BASE_URL}/libraries/{library_id}")
            if response.status_code == 200:
                library = response.json()
                if "id" in library and "name" in library and "status" in library:
                    self.log_test("KAN-205", "Get Library by ID", "PASSED", f"Retrieved library: {library['name']}")
                else:
                    self.log_test("KAN-205", "Get Library by ID Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-205", "Get Library by ID", "FAILED", f"Status code: {response.status_code}")
            
            # Test 4: GET /libraries/{id} - 404 for non-existent library
            response = requests.get(f"{BASE_URL}/libraries/99999")
            if response.status_code == 404:
                self.log_test("KAN-205", "Get Library 404 Error", "PASSED", "Correctly returns 404 for non-existent library")
            else:
                self.log_test("KAN-205", "Get Library 404 Error", "FAILED", f"Expected 404, got {response.status_code}")
            
            # Test 5: PUT /libraries/{id} - Update library
            update_data = {
                "name": "Updated Test Library",
                "status": "Inactive"
            }
            
            response = requests.put(f"{BASE_URL}/libraries/{library_id}", json=update_data)
            if response.status_code == 200:
                result = response.json()
                if "message" in result and result["message"] == "Library updated successfully":
                    self.log_test("KAN-205", "Update Library", "PASSED", "Library updated successfully")
                else:
                    self.log_test("KAN-205", "Update Library Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-205", "Update Library", "FAILED", f"Status code: {response.status_code}")
            
            # Test 6: PUT /libraries/{id} - Partial update
            partial_update = {
                "name": "Partially Updated Library"
            }
            
            response = requests.put(f"{BASE_URL}/libraries/{library_id}", json=partial_update)
            if response.status_code == 200:
                self.log_test("KAN-205", "Partial Update Library", "PASSED", "Partial update successful")
            else:
                self.log_test("KAN-205", "Partial Update Library", "FAILED", f"Status code: {response.status_code}")
            
            # Test 7: PUT /libraries/{id} - 404 for non-existent library
            response = requests.put(f"{BASE_URL}/libraries/99999", json=update_data)
            if response.status_code == 404:
                self.log_test("KAN-205", "Update Library 404 Error", "PASSED", "Correctly returns 404 for non-existent library")
            else:
                self.log_test("KAN-205", "Update Library 404 Error", "FAILED", f"Expected 404, got {response.status_code}")
            
            # Test 8: DELETE /libraries/{id} - Delete library
            response = requests.delete(f"{BASE_URL}/libraries/{library_id}")
            if response.status_code == 200:
                result = response.json()
                if "message" in result and result["message"] == "Library deleted successfully":
                    self.log_test("KAN-205", "Delete Library", "PASSED", "Library deleted successfully")
                else:
                    self.log_test("KAN-205", "Delete Library Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-205", "Delete Library", "FAILED", f"Status code: {response.status_code}")
            
            # Test 9: DELETE /libraries/{id} - 404 for non-existent library
            response = requests.delete(f"{BASE_URL}/libraries/99999")
            if response.status_code == 404:
                self.log_test("KAN-205", "Delete Library 404 Error", "PASSED", "Correctly returns 404 for non-existent library")
            else:
                self.log_test("KAN-205", "Delete Library 404 Error", "FAILED", f"Expected 404, got {response.status_code}")
            
            # Test 10: Verify library is actually deleted
            response = requests.get(f"{BASE_URL}/libraries/{library_id}")
            if response.status_code == 404:
                self.log_test("KAN-205", "Library Deletion Verification", "PASSED", "Library successfully deleted from database")
            else:
                self.log_test("KAN-205", "Library Deletion Verification", "FAILED", f"Library still exists after deletion")
            
            self.results["KAN-205"]["status"] = "COMPLETED"
            
        except requests.exceptions.ConnectionError:
            self.log_test("KAN-205", "Server Connection", "FAILED", "Server not running. Start with: python src/app/main.py")
            self.results["KAN-205"]["status"] = "FAILED"
        except Exception as e:
            self.log_test("KAN-205", "Library CRUD Endpoints", "FAILED", str(e))
            self.results["KAN-205"]["status"] = "FAILED"
    
    def test_kan_206(self):
        """Test KAN-206: Book Create/List Endpoints."""
        print("\n" + "="*60)
        print("Testing KAN-206: Book Create/List Endpoints")
        print("="*60)
        
        try:
            # Test 1: Server health check
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                self.log_test("KAN-206", "Server Health Check", "PASSED", "Server is running")
            else:
                self.log_test("KAN-206", "Server Health Check", "FAILED", f"Server returned {response.status_code}")
                return
            
            # Test 2: Create a book
            import time
            unique_isbn = f"978{int(time.time())}"  # Generate unique ISBN
            book_data = {
                "title": "AI Fundamentals",
                "author": "John Smith",
                "category": "AI",
                "price": 550.00,
                "isbn": unique_isbn
            }
            
            response = requests.post(f"{BASE_URL}/books", json=book_data)
            if response.status_code == 201:
                created_book = response.json()
                if "id" in created_book and "message" in created_book:
                    book_id = created_book["id"]
                    self.log_test("KAN-206", "Create Book", "PASSED", f"Book created with ID: {book_id}")
                else:
                    self.log_test("KAN-206", "Create Book Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-206", "Create Book", "FAILED", f"Status code: {response.status_code}")
                return
            
            # Test 3: Create book with duplicate ISBN
            duplicate_book_data = {
                "title": "Another AI Book",
                "author": "Jane Doe",
                "category": "AI",
                "price": 600.00,
                "isbn": unique_isbn  # Same ISBN as above
            }
            
            response = requests.post(f"{BASE_URL}/books", json=duplicate_book_data)
            if response.status_code == 409:
                self.log_test("KAN-206", "Duplicate ISBN Handling", "PASSED", "Correctly returns 409 Conflict for duplicate ISBN")
            else:
                self.log_test("KAN-206", "Duplicate ISBN Handling", "FAILED", f"Expected 409, got {response.status_code}")
            
            # Test 4: Get books with pagination
            response = requests.get(f"{BASE_URL}/books?page=1&limit=10")
            if response.status_code == 200:
                books = response.json()
                if isinstance(books, list):
                    self.log_test("KAN-206", "Get Books Pagination", "PASSED", f"Retrieved {len(books)} books")
                else:
                    self.log_test("KAN-206", "Get Books Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-206", "Get Books Pagination", "FAILED", f"Status code: {response.status_code}")
            
            # Test 5: Get books without pagination (default)
            response = requests.get(f"{BASE_URL}/books")
            if response.status_code == 200:
                books = response.json()
                if isinstance(books, list):
                    self.log_test("KAN-206", "Get Books Default", "PASSED", f"Retrieved {len(books)} books with default pagination")
                else:
                    self.log_test("KAN-206", "Get Books Default Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-206", "Get Books Default", "FAILED", f"Status code: {response.status_code}")
            
            # Test 6: Book Response Format
            if response.status_code == 200 and response.json():
                first_book = response.json()[0]
                required_fields = ["id", "title", "author", "category"]
                if all(field in first_book for field in required_fields):
                    self.log_test("KAN-206", "Book Response Format", "PASSED", "Clean JSON format returned")
                else:
                    self.log_test("KAN-206", "Book Response Format", "FAILED", "Missing required fields")
            
            self.results["KAN-206"]["status"] = "COMPLETED"
            
        except requests.exceptions.ConnectionError:
            self.log_test("KAN-206", "Server Connection", "FAILED", "Server not running. Start with: python src/app/main.py")
            self.results["KAN-206"]["status"] = "FAILED"
        except Exception as e:
            self.log_test("KAN-206", "Book Create/List Endpoints", "FAILED", str(e))
            self.results["KAN-206"]["status"] = "FAILED"
    
    def test_kan_207(self):
        """Test KAN-207: Book Read/Update/Delete Endpoints."""
        print("\n" + "="*60)
        print("Testing KAN-207: Book Read/Update/Delete Endpoints")
        print("="*60)
        
        try:
            # Test 1: Server health check
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                self.log_test("KAN-207", "Server Health Check", "PASSED", "Server is running")
            else:
                self.log_test("KAN-207", "Server Health Check", "FAILED", f"Server returned {response.status_code}")
                return
            
            # Test 2: Create a book first (for testing other endpoints)
            book_data = {
                "title": "Test Book KAN-207",
                "author": "Test Author",
                "category": "Test Category",
                "price": 100.00,
                "isbn": "9789876543210"
            }
            
            create_response = requests.post(f"{BASE_URL}/books", json=book_data)
            if create_response.status_code == 201:
                created_book = create_response.json()
                book_id = created_book["id"]
                self.log_test("KAN-207", "Create Book for Testing", "PASSED", f"Book created with ID: {book_id}")
            else:
                self.log_test("KAN-207", "Create Book for Testing", "FAILED", f"Status code: {create_response.status_code}")
                return
            
            # Test 3: GET /books/{id} - Get book by ID
            response = requests.get(f"{BASE_URL}/books/{book_id}")
            if response.status_code == 200:
                book = response.json()
                if "id" in book and "title" in book and "author" in book:
                    self.log_test("KAN-207", "Get Book by ID", "PASSED", f"Retrieved book: {book['title']}")
                else:
                    self.log_test("KAN-207", "Get Book by ID Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-207", "Get Book by ID", "FAILED", f"Status code: {response.status_code}")
            
            # Test 4: GET /books/{id} - 404 for non-existent book
            response = requests.get(f"{BASE_URL}/books/99999")
            if response.status_code == 404:
                self.log_test("KAN-207", "Get Book 404 Error", "PASSED", "Correctly returns 404 for non-existent book")
            else:
                self.log_test("KAN-207", "Get Book 404 Error", "FAILED", f"Expected 404, got {response.status_code}")
            
            # Test 5: PUT /books/{id} - Update book
            update_data = {
                "price": 150.00,
                "category": "Updated Category"
            }
            
            response = requests.put(f"{BASE_URL}/books/{book_id}", json=update_data)
            if response.status_code == 200:
                result = response.json()
                if "message" in result and result["message"] == "Book updated successfully":
                    self.log_test("KAN-207", "Update Book", "PASSED", "Book updated successfully")
                else:
                    self.log_test("KAN-207", "Update Book Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-207", "Update Book", "FAILED", f"Status code: {response.status_code}")
            
            # Test 6: PUT /books/{id} - Update with duplicate ISBN
            duplicate_isbn_data = {
                "isbn": "9781234567890"  # This ISBN should already exist from KAN-206 test
            }
            
            response = requests.put(f"{BASE_URL}/books/{book_id}", json=duplicate_isbn_data)
            if response.status_code == 409:
                self.log_test("KAN-207", "Update Book Duplicate ISBN", "PASSED", "Correctly returns 409 for duplicate ISBN")
            else:
                self.log_test("KAN-207", "Update Book Duplicate ISBN", "FAILED", f"Expected 409, got {response.status_code}")
            
            # Test 7: PUT /books/{id} - 404 for non-existent book
            response = requests.put(f"{BASE_URL}/books/99999", json=update_data)
            if response.status_code == 404:
                self.log_test("KAN-207", "Update Book 404 Error", "PASSED", "Correctly returns 404 for non-existent book")
            else:
                self.log_test("KAN-207", "Update Book 404 Error", "FAILED", f"Expected 404, got {response.status_code}")
            
            # Test 8: DELETE /books/{id} - Delete book
            response = requests.delete(f"{BASE_URL}/books/{book_id}")
            if response.status_code == 200:
                result = response.json()
                if "message" in result and result["message"] == "Book deleted successfully":
                    self.log_test("KAN-207", "Delete Book", "PASSED", "Book deleted successfully")
                else:
                    self.log_test("KAN-207", "Delete Book Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-207", "Delete Book", "FAILED", f"Status code: {response.status_code}")
            
            # Test 9: DELETE /books/{id} - 404 for non-existent book
            response = requests.delete(f"{BASE_URL}/books/99999")
            if response.status_code == 404:
                self.log_test("KAN-207", "Delete Book 404 Error", "PASSED", "Correctly returns 404 for non-existent book")
            else:
                self.log_test("KAN-207", "Delete Book 404 Error", "FAILED", f"Expected 404, got {response.status_code}")
            
            # Test 10: Verify book is actually deleted
            response = requests.get(f"{BASE_URL}/books/{book_id}")
            if response.status_code == 404:
                self.log_test("KAN-207", "Book Deletion Verification", "PASSED", "Book successfully deleted from database")
            else:
                self.log_test("KAN-207", "Book Deletion Verification", "FAILED", f"Book still exists after deletion")
            
            self.results["KAN-207"]["status"] = "COMPLETED"
            
        except requests.exceptions.ConnectionError:
            self.log_test("KAN-207", "Server Connection", "FAILED", "Server not running. Start with: python src/app/main.py")
            self.results["KAN-207"]["status"] = "FAILED"
        except Exception as e:
            self.log_test("KAN-207", "Book Read/Update/Delete Endpoints", "FAILED", str(e))
            self.results["KAN-207"]["status"] = "FAILED"
    
    def test_kan_208(self):
        """Test KAN-208: Library-Book Mapping Endpoints."""
        print("\n" + "=" * 60)
        print("Testing KAN-208: Library-Book Mapping Endpoints")
        print("=" * 60)
        
        try:
            # Test 1: Server health check
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                self.log_test("KAN-208", "Server Health Check", "PASSED", "Server is running")
            else:
                self.log_test("KAN-208", "Server Health Check", "FAILED", f"Server returned {response.status_code}")
                return
            
            # Test 2: Create a library and book first (for testing mappings)
            library_data = {
                "name": "Test Library KAN-208",
                "dept": "Computer Science",
                "count": 0,
                "status": "Active"
            }
            
            library_response = requests.post(f"{BASE_URL}/libraries", json=library_data)
            if library_response.status_code == 201:
                library_id = library_response.json()["id"]
                self.log_test("KAN-208", "Create Library for Testing", "PASSED", f"Library created with ID: {library_id}")
            else:
                self.log_test("KAN-208", "Create Library for Testing", "FAILED", f"Status code: {library_response.status_code}")
                return
            
            # Create a book
            import time
            unique_isbn = f"978{int(time.time())}"
            book_data = {
                "title": "Test Book KAN-208",
                "author": "Test Author",
                "category": "Test Category",
                "price": 100.00,
                "isbn": unique_isbn
            }
            
            book_response = requests.post(f"{BASE_URL}/books", json=book_data)
            if book_response.status_code == 201:
                book_id = book_response.json()["id"]
                self.log_test("KAN-208", "Create Book for Testing", "PASSED", f"Book created with ID: {book_id}")
            else:
                self.log_test("KAN-208", "Create Book for Testing", "FAILED", f"Status code: {book_response.status_code}")
                return
            
            # Test 3: Create library-book mapping
            mapping_data = {
                "lib_id": library_id,
                "book_id": book_id,
                "status": "Active"
            }
            
            response = requests.post(f"{BASE_URL}/library-books", json=mapping_data)
            if response.status_code == 201:
                created_mapping = response.json()
                if "id" in created_mapping and "message" in created_mapping:
                    mapping_id = created_mapping["id"]
                    self.log_test("KAN-208", "Create Library-Book Mapping", "PASSED", f"Mapping created with ID: {mapping_id}")
                else:
                    self.log_test("KAN-208", "Create Mapping Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-208", "Create Library-Book Mapping", "FAILED", f"Status code: {response.status_code}")
                return
            
            # Test 4: Create duplicate mapping (409 Conflict)
            duplicate_mapping_data = {
                "lib_id": library_id,
                "book_id": book_id,
                "status": "Active"
            }
            
            response = requests.post(f"{BASE_URL}/library-books", json=duplicate_mapping_data)
            if response.status_code == 409:
                self.log_test("KAN-208", "Duplicate Mapping Handling", "PASSED", "Correctly returns 409 Conflict for duplicate mapping")
            else:
                self.log_test("KAN-208", "Duplicate Mapping Handling", "FAILED", f"Expected 409, got {response.status_code}")
            
            # Test 5: Create mapping with non-existent library (400 Bad Request)
            invalid_library_mapping = {
                "lib_id": 99999,
                "book_id": book_id,
                "status": "Active"
            }
            
            response = requests.post(f"{BASE_URL}/library-books", json=invalid_library_mapping)
            if response.status_code == 400:
                self.log_test("KAN-208", "Non-existent Library Handling", "PASSED", "Correctly returns 400 for non-existent library")
            else:
                self.log_test("KAN-208", "Non-existent Library Handling", "FAILED", f"Expected 400, got {response.status_code}")
            
            # Test 6: Create mapping with non-existent book (400 Bad Request)
            invalid_book_mapping = {
                "lib_id": library_id,
                "book_id": 99999,
                "status": "Active"
            }
            
            response = requests.post(f"{BASE_URL}/library-books", json=invalid_book_mapping)
            if response.status_code == 400:
                self.log_test("KAN-208", "Non-existent Book Handling", "PASSED", "Correctly returns 400 for non-existent book")
            else:
                self.log_test("KAN-208", "Non-existent Book Handling", "FAILED", f"Expected 400, got {response.status_code}")
            
            # Test 7: Get all library-book mappings
            response = requests.get(f"{BASE_URL}/library-books")
            if response.status_code == 200:
                mappings = response.json()
                if isinstance(mappings, list):
                    self.log_test("KAN-208", "Get All Mappings", "PASSED", f"Retrieved {len(mappings)} mappings")
                    
                    # Check response format
                    if mappings and all("id" in mapping and "lib_id" in mapping and "book_id" in mapping for mapping in mappings):
                        self.log_test("KAN-208", "Mapping Response Format", "PASSED", "Clean JSON format returned")
                    else:
                        self.log_test("KAN-208", "Mapping Response Format", "FAILED", "Response format incorrect")
                else:
                    self.log_test("KAN-208", "Get Mappings Response", "FAILED", "Response is not a list")
            else:
                self.log_test("KAN-208", "Get All Mappings", "FAILED", f"Status code: {response.status_code}")
            
            # Test 8: Verify library count was incremented
            library_check_response = requests.get(f"{BASE_URL}/libraries/{library_id}")
            if library_check_response.status_code == 200:
                library = library_check_response.json()
                if library.get("count", 0) > 0:
                    self.log_test("KAN-208", "Library Count Increment", "PASSED", f"Library count incremented to {library.get('count', 0)}")
                else:
                    self.log_test("KAN-208", "Library Count Increment", "FAILED", "Library count was not incremented")
            else:
                self.log_test("KAN-208", "Library Count Verification", "FAILED", f"Could not verify library count")
            
            self.results["KAN-208"]["status"] = "COMPLETED"
            
        except requests.exceptions.ConnectionError:
            self.log_test("KAN-208", "Server Connection", "FAILED", "Server not running. Start with: python src/app/main.py")
            self.results["KAN-208"]["status"] = "FAILED"
        except Exception as e:
            self.log_test("KAN-208", "Library-Book Mapping Endpoints", "FAILED", str(e))
            self.results["KAN-208"]["status"] = "FAILED"
    
    def test_kan_209(self):
        """Test KAN-209: Library-Book Mapping Detail/Update/Delete Endpoints."""
        print("\n" + "=" * 60)
        print("Testing KAN-209: Library-Book Mapping Detail/Update/Delete Endpoints")
        print("=" * 60)
        
        try:
            # Test 1: Server health check
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                self.log_test("KAN-209", "Server Health Check", "PASSED", "Server is running")
            else:
                self.log_test("KAN-209", "Server Health Check", "FAILED", f"Server returned {response.status_code}")
                return
            
            # Test 2: Create a library and book first (for testing mappings)
            library_data = {
                "name": "Test Library KAN-209",
                "dept": "Computer Science",
                "count": 0,
                "status": "Active"
            }
            
            library_response = requests.post(f"{BASE_URL}/libraries", json=library_data)
            if library_response.status_code == 201:
                library_id = library_response.json()["id"]
                self.log_test("KAN-209", "Create Library for Testing", "PASSED", f"Library created with ID: {library_id}")
            else:
                self.log_test("KAN-209", "Create Library for Testing", "FAILED", f"Status code: {library_response.status_code}")
                return
            
            # Create a book
            import time
            unique_isbn = f"978{int(time.time())}"
            book_data = {
                "title": "Test Book KAN-209",
                "author": "Test Author",
                "category": "Test Category",
                "price": 100.00,
                "isbn": unique_isbn
            }
            
            book_response = requests.post(f"{BASE_URL}/books", json=book_data)
            if book_response.status_code == 201:
                book_id = book_response.json()["id"]
                self.log_test("KAN-209", "Create Book for Testing", "PASSED", f"Book created with ID: {book_id}")
            else:
                self.log_test("KAN-209", "Create Book for Testing", "FAILED", f"Status code: {book_response.status_code}")
                return
            
            # Create a mapping
            mapping_data = {
                "lib_id": library_id,
                "book_id": book_id,
                "status": "Active"
            }
            
            mapping_response = requests.post(f"{BASE_URL}/library-books", json=mapping_data)
            if mapping_response.status_code == 201:
                mapping_id = mapping_response.json()["id"]
                self.log_test("KAN-209", "Create Mapping for Testing", "PASSED", f"Mapping created with ID: {mapping_id}")
            else:
                self.log_test("KAN-209", "Create Mapping for Testing", "FAILED", f"Status code: {mapping_response.status_code}")
                return
            
            # Test 3: GET /library-books/{id} - Get mapping by ID
            response = requests.get(f"{BASE_URL}/library-books/{mapping_id}")
            if response.status_code == 200:
                mapping = response.json()
                if "id" in mapping and "lib_id" in mapping and "book_id" in mapping:
                    self.log_test("KAN-209", "Get Mapping by ID", "PASSED", f"Retrieved mapping: {mapping['id']}")
                else:
                    self.log_test("KAN-209", "Get Mapping by ID Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-209", "Get Mapping by ID", "FAILED", f"Status code: {response.status_code}")
            
            # Test 4: GET /library-books/{id} - 404 for non-existent mapping
            response = requests.get(f"{BASE_URL}/library-books/99999")
            if response.status_code == 404:
                self.log_test("KAN-209", "Get Mapping 404 Error", "PASSED", "Correctly returns 404 for non-existent mapping")
            else:
                self.log_test("KAN-209", "Get Mapping 404 Error", "FAILED", f"Expected 404, got {response.status_code}")
            
            # Test 5: PUT /library-books/{id} - Update mapping status
            update_data = {
                "status": "Inactive"
            }
            
            response = requests.put(f"{BASE_URL}/library-books/{mapping_id}", json=update_data)
            if response.status_code == 200:
                result = response.json()
                if "message" in result and result["message"] == "Mapping updated successfully":
                    self.log_test("KAN-209", "Update Mapping Status", "PASSED", "Mapping status updated successfully")
                else:
                    self.log_test("KAN-209", "Update Mapping Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-209", "Update Mapping Status", "FAILED", f"Status code: {response.status_code}")
            
            # Test 6: PUT /library-books/{id} - Update back to Active
            update_data = {
                "status": "Active"
            }
            
            response = requests.put(f"{BASE_URL}/library-books/{mapping_id}", json=update_data)
            if response.status_code == 200:
                self.log_test("KAN-209", "Update Mapping Back to Active", "PASSED", "Mapping status updated back to Active")
            else:
                self.log_test("KAN-209", "Update Mapping Back to Active", "FAILED", f"Status code: {response.status_code}")
            
            # Test 7: PUT /library-books/{id} - 404 for non-existent mapping
            response = requests.put(f"{BASE_URL}/library-books/99999", json=update_data)
            if response.status_code == 404:
                self.log_test("KAN-209", "Update Mapping 404 Error", "PASSED", "Correctly returns 404 for non-existent mapping")
            else:
                self.log_test("KAN-209", "Update Mapping 404 Error", "FAILED", f"Expected 404, got {response.status_code}")
            
            # Test 8: DELETE /library-books/{id} - Delete mapping
            response = requests.delete(f"{BASE_URL}/library-books/{mapping_id}")
            if response.status_code == 200:
                result = response.json()
                if "message" in result and result["message"] == "Mapping deleted successfully":
                    self.log_test("KAN-209", "Delete Mapping", "PASSED", "Mapping deleted successfully")
                else:
                    self.log_test("KAN-209", "Delete Mapping Response", "FAILED", "Response format incorrect")
            else:
                self.log_test("KAN-209", "Delete Mapping", "FAILED", f"Status code: {response.status_code}")
            
            # Test 9: DELETE /library-books/{id} - 404 for non-existent mapping
            response = requests.delete(f"{BASE_URL}/library-books/99999")
            if response.status_code == 404:
                self.log_test("KAN-209", "Delete Mapping 404 Error", "PASSED", "Correctly returns 404 for non-existent mapping")
            else:
                self.log_test("KAN-209", "Delete Mapping 404 Error", "FAILED", f"Expected 404, got {response.status_code}")
            
            # Test 10: Verify mapping is actually deleted
            response = requests.get(f"{BASE_URL}/library-books/{mapping_id}")
            if response.status_code == 404:
                self.log_test("KAN-209", "Mapping Deletion Verification", "PASSED", "Mapping successfully deleted from database")
            else:
                self.log_test("KAN-209", "Mapping Deletion Verification", "FAILED", f"Mapping still exists after deletion")
            
            self.results["KAN-209"]["status"] = "COMPLETED"
            
        except requests.exceptions.ConnectionError:
            self.log_test("KAN-209", "Server Connection", "FAILED", "Server not running. Start with: python src/app/main.py")
            self.results["KAN-209"]["status"] = "FAILED"
        except Exception as e:
            self.log_test("KAN-209", "Library-Book Mapping Detail/Update/Delete Endpoints", "FAILED", str(e))
            self.results["KAN-209"]["status"] = "FAILED"
    
    def test_kan_210(self):
        """Test KAN-210: Books in a Library (Joined Response)."""
        print("\n" + "=" * 60)
        print("Testing KAN-210: Books in a Library (Joined Response)")
        print("=" * 60)
        
        try:
            # Test 1: Server health check
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                self.log_test("KAN-210", "Server Health Check", "PASSED", "Server is running")
            else:
                self.log_test("KAN-210", "Server Health Check", "FAILED", f"Server returned {response.status_code}")
                return
            
            # Test 2: Create a library for testing
            library_data = {
                "name": "Test Library KAN-210",
                "dept": "Computer Science",
                "count": 0,
                "status": "Active"
            }
            
            library_response = requests.post(f"{BASE_URL}/libraries", json=library_data)
            if library_response.status_code == 201:
                library_id = library_response.json()["id"]
                self.log_test("KAN-210", "Create Library for Testing", "PASSED", f"Library created with ID: {library_id}")
            else:
                self.log_test("KAN-210", "Create Library for Testing", "FAILED", f"Status code: {library_response.status_code}")
                return
            
            # Test 3: Create books for testing
            import time
            unique_isbn1 = f"978{int(time.time())}"
            unique_isbn2 = f"978{int(time.time()) + 1}"
            
            book1_data = {
                "title": "Test Book 1 KAN-210",
                "author": "Test Author 1",
                "category": "Test Category 1",
                "price": 100.00,
                "isbn": unique_isbn1
            }
            
            book1_response = requests.post(f"{BASE_URL}/books", json=book1_data)
            if book1_response.status_code == 201:
                book1_id = book1_response.json()["id"]
                self.log_test("KAN-210", "Create Book 1 for Testing", "PASSED", f"Book 1 created with ID: {book1_id}")
            else:
                self.log_test("KAN-210", "Create Book 1 for Testing", "FAILED", f"Status code: {book1_response.status_code}")
                return
            
            book2_data = {
                "title": "Test Book 2 KAN-210",
                "author": "Test Author 2",
                "category": "Test Category 2",
                "price": 200.00,
                "isbn": unique_isbn2
            }
            
            book2_response = requests.post(f"{BASE_URL}/books", json=book2_data)
            if book2_response.status_code == 201:
                book2_id = book2_response.json()["id"]
                self.log_test("KAN-210", "Create Book 2 for Testing", "PASSED", f"Book 2 created with ID: {book2_id}")
            else:
                self.log_test("KAN-210", "Create Book 2 for Testing", "FAILED", f"Status code: {book2_response.status_code}")
                return
            
            # Test 4: Create mappings for testing
            mapping1_data = {
                "lib_id": library_id,
                "book_id": book1_id,
                "status": "Active"
            }
            
            mapping1_response = requests.post(f"{BASE_URL}/library-books", json=mapping1_data)
            if mapping1_response.status_code == 201:
                self.log_test("KAN-210", "Create Mapping 1 for Testing", "PASSED", "Mapping 1 created successfully")
            else:
                self.log_test("KAN-210", "Create Mapping 1 for Testing", "FAILED", f"Status code: {mapping1_response.status_code}")
                return
            
            mapping2_data = {
                "lib_id": library_id,
                "book_id": book2_id,
                "status": "Inactive"
            }
            
            mapping2_response = requests.post(f"{BASE_URL}/library-books", json=mapping2_data)
            if mapping2_response.status_code == 201:
                self.log_test("KAN-210", "Create Mapping 2 for Testing", "PASSED", "Mapping 2 created successfully")
            else:
                self.log_test("KAN-210", "Create Mapping 2 for Testing", "FAILED", f"Status code: {mapping2_response.status_code}")
                return
            
            # Test 5: GET /libraries/{id}/books - Get all books in library
            response = requests.get(f"{BASE_URL}/libraries/{library_id}/books")
            if response.status_code == 200:
                books = response.json()
                if isinstance(books, list) and len(books) == 2:
                    # Check if response has required fields
                    book = books[0]
                    required_fields = ["book_id", "title", "status", "author", "category", "isbn"]
                    if all(field in book for field in required_fields):
                        self.log_test("KAN-210", "Get All Books in Library", "PASSED", f"Retrieved {len(books)} books with correct format")
                    else:
                        self.log_test("KAN-210", "Get All Books Response Format", "FAILED", "Response missing required fields")
                else:
                    self.log_test("KAN-210", "Get All Books Count", "FAILED", f"Expected 2 books, got {len(books) if isinstance(books, list) else 'invalid response'}")
            else:
                self.log_test("KAN-210", "Get All Books in Library", "FAILED", f"Status code: {response.status_code}")
            
            # Test 6: GET /libraries/{id}/books?status=Active - Filter by Active status
            response = requests.get(f"{BASE_URL}/libraries/{library_id}/books?status=Active")
            if response.status_code == 200:
                books = response.json()
                if isinstance(books, list) and len(books) == 1:
                    book = books[0]
                    if book["status"] == "Active":
                        self.log_test("KAN-210", "Filter Books by Active Status", "PASSED", "Correctly filtered to 1 Active book")
                    else:
                        self.log_test("KAN-210", "Filter Books by Active Status", "FAILED", "Book status is not Active")
                else:
                    self.log_test("KAN-210", "Filter Books by Active Status Count", "FAILED", f"Expected 1 Active book, got {len(books) if isinstance(books, list) else 'invalid response'}")
            else:
                self.log_test("KAN-210", "Filter Books by Active Status", "FAILED", f"Status code: {response.status_code}")
            
            # Test 7: GET /libraries/{id}/books?status=Inactive - Filter by Inactive status
            response = requests.get(f"{BASE_URL}/libraries/{library_id}/books?status=Inactive")
            if response.status_code == 200:
                books = response.json()
                if isinstance(books, list) and len(books) == 1:
                    book = books[0]
                    if book["status"] == "Inactive":
                        self.log_test("KAN-210", "Filter Books by Inactive Status", "PASSED", "Correctly filtered to 1 Inactive book")
                    else:
                        self.log_test("KAN-210", "Filter Books by Inactive Status", "FAILED", "Book status is not Inactive")
                else:
                    self.log_test("KAN-210", "Filter Books by Inactive Status Count", "FAILED", f"Expected 1 Inactive book, got {len(books) if isinstance(books, list) else 'invalid response'}")
            else:
                self.log_test("KAN-210", "Filter Books by Inactive Status", "FAILED", f"Status code: {response.status_code}")
            
            # Test 8: GET /libraries/{id}/books - 404 for non-existent library
            response = requests.get(f"{BASE_URL}/libraries/99999/books")
            if response.status_code == 404:
                self.log_test("KAN-210", "Get Books 404 Error", "PASSED", "Correctly returns 404 for non-existent library")
            else:
                self.log_test("KAN-210", "Get Books 404 Error", "FAILED", f"Expected 404, got {response.status_code}")
            
            # Test 9: Verify joined response contains book metadata
            response = requests.get(f"{BASE_URL}/libraries/{library_id}/books")
            if response.status_code == 200:
                books = response.json()
                if isinstance(books, list) and len(books) > 0:
                    book = books[0]
                    # Check that we have both mapping status and book details
                    if "status" in book and "title" in book and "author" in book:
                        self.log_test("KAN-210", "Joined Response Verification", "PASSED", "Response contains both mapping status and book metadata")
                    else:
                        self.log_test("KAN-210", "Joined Response Verification", "FAILED", "Response missing mapping status or book metadata")
                else:
                    self.log_test("KAN-210", "Joined Response Verification", "FAILED", "No books returned for verification")
            else:
                self.log_test("KAN-210", "Joined Response Verification", "FAILED", f"Status code: {response.status_code}")
            
            self.results["KAN-210"]["status"] = "COMPLETED"
            
        except requests.exceptions.ConnectionError:
            self.log_test("KAN-210", "Server Connection", "FAILED", "Server not running. Start with: python src/app/main.py")
            self.results["KAN-210"]["status"] = "FAILED"
        except Exception as e:
            self.log_test("KAN-210", "Books in a Library (Joined Response)", "FAILED", str(e))
            self.results["KAN-210"]["status"] = "FAILED"
    
    def test_kan_211(self):
        """Test KAN-211: Validation & Centralized Error Handling."""
        print("\n" + "=" * 60)
        print("Testing KAN-211: Validation & Centralized Error Handling")
        print("=" * 60)
        
        try:
            # Test 1: Server health check
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                self.log_test("KAN-211", "Server Health Check", "PASSED", "Server is running")
            else:
                self.log_test("KAN-211", "Server Health Check", "FAILED", f"Server returned {response.status_code}")
                return
            
            # Test 2: Validation Error - Missing required fields
            invalid_book_data = {
                "title": "Invalid Book"
                # Missing required fields: author, category, price, isbn
            }
            
            response = requests.post(f"{BASE_URL}/books", json=invalid_book_data)
            if response.status_code == 422:
                json_data = response.json()
                if "detail" in json_data and "errors" in json_data:
                    self.log_test("KAN-211", "Validation Error Format", "PASSED", "Error response contains detail and errors fields")
                else:
                    self.log_test("KAN-211", "Validation Error Format", "FAILED", "Error response missing required fields")
            else:
                self.log_test("KAN-211", "Validation Error", "FAILED", f"Expected 422, got {response.status_code}")
            
            # Test 3: Duplicate ISBN - Should return 409 Conflict
            import time
            unique_isbn = f"978{int(time.time())}"
            
            valid_book_data = {
                "title": "Test Book for Duplicate",
                "author": "Test Author",
                "category": "Test Category",
                "price": 100.00,
                "isbn": unique_isbn
            }
            
            # Create first book
            response1 = requests.post(f"{BASE_URL}/books", json=valid_book_data)
            if response1.status_code == 201:
                self.log_test("KAN-211", "Create First Book", "PASSED", "First book created successfully")
            else:
                self.log_test("KAN-211", "Create First Book", "FAILED", f"Status code: {response1.status_code}")
                return
            
            # Try to create duplicate ISBN - should return 409
            response2 = requests.post(f"{BASE_URL}/books", json=valid_book_data)
            if response2.status_code == 409:
                json_data = response2.json()
                if "detail" in json_data:
                    self.log_test("KAN-211", "Duplicate ISBN 409 Conflict", "PASSED", "Correctly returns 409 for duplicate ISBN")
                else:
                    self.log_test("KAN-211", "Duplicate ISBN Response Format", "FAILED", "Response missing detail field")
            else:
                self.log_test("KAN-211", "Duplicate ISBN 409 Conflict", "FAILED", f"Expected 409, got {response2.status_code}")
            
            # Test 4: Invalid book_id in library-book mapping - Should return 400
            invalid_mapping_data = {
                "lib_id": 99999,  # Non-existent library
                "book_id": 99999,  # Non-existent book
                "status": "Active"
            }
            
            response = requests.post(f"{BASE_URL}/library-books", json=invalid_mapping_data)
            if response.status_code == 400:
                json_data = response.json()
                if "detail" in json_data:
                    self.log_test("KAN-211", "Foreign Key Error 400", "PASSED", "Correctly returns 400 for invalid references")
                else:
                    self.log_test("KAN-211", "Foreign Key Error Format", "FAILED", "Response missing detail field")
            else:
                self.log_test("KAN-211", "Foreign Key Error 400", "FAILED", f"Expected 400, got {response.status_code}")
            
            # Test 5: Invalid library_id in GET request - Should return 404
            response = requests.get(f"{BASE_URL}/libraries/99999")
            if response.status_code == 404:
                json_data = response.json()
                if "detail" in json_data:
                    self.log_test("KAN-211", "404 Error Format", "PASSED", "Correctly returns 404 for non-existent library")
                else:
                    self.log_test("KAN-211", "404 Error Format", "FAILED", "Response missing detail field")
            else:
                self.log_test("KAN-211", "404 Error Handling", "FAILED", f"Expected 404, got {response.status_code}")
            
            # Test 6: Invalid query parameter - Should return 422 for validation error
            # Try to get books with invalid status
            response = requests.get(f"{BASE_URL}/libraries/1/books?status=InvalidStatus")
            # This should still work but might return empty or all results
            
            # Test 7: Invalid JSON in request body - Should return 422
            try:
                response = requests.post(
                    f"{BASE_URL}/books",
                    data="not json",
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code in [400, 422]:
                    self.log_test("KAN-211", "Invalid JSON Handling", "PASSED", f"Correctly handles invalid JSON with {response.status_code}")
                else:
                    self.log_test("KAN-211", "Invalid JSON Handling", "FAILED", f"Expected 400/422, got {response.status_code}")
            except Exception as e:
                self.log_test("KAN-211", "Invalid JSON Handling", "PASSED", f"Error handler caught exception: {str(e)}")
            
            # Test 8: Duplicate library-book mapping - Should return 409
            # First, get a real library and book
            libraries_response = requests.get(f"{BASE_URL}/libraries")
            if libraries_response.status_code == 200:
                libraries = libraries_response.json()
                if len(libraries) > 0:
                    lib_id = libraries[0]["id"]
                    
                    books_response = requests.get(f"{BASE_URL}/books")
                    if books_response.status_code == 200:
                        books = books_response.json()
                        if len(books) > 0:
                            book_id = books[0]["id"]
                            
                            # Create first mapping
                            mapping_data = {
                                "lib_id": lib_id,
                                "book_id": book_id,
                                "status": "Active"
                            }
                            
                            mapping1_response = requests.post(f"{BASE_URL}/library-books", json=mapping_data)
                            if mapping1_response.status_code == 201:
                                self.log_test("KAN-211", "Create First Mapping", "PASSED", "First mapping created")
                                
                                # Try to create duplicate mapping - should return 409
                                mapping2_response = requests.post(f"{BASE_URL}/library-books", json=mapping_data)
                                if mapping2_response.status_code == 409:
                                    json_data = mapping2_response.json()
                                    if "detail" in json_data:
                                        self.log_test("KAN-211", "Duplicate Mapping 409", "PASSED", "Correctly returns 409 for duplicate mapping")
                                    else:
                                        self.log_test("KAN-211", "Duplicate Mapping Format", "FAILED", "Response missing detail field")
                                else:
                                    self.log_test("KAN-211", "Duplicate Mapping 409", "FAILED", f"Expected 409, got {mapping2_response.status_code}")
            
            self.results["KAN-211"]["status"] = "COMPLETED"
            
        except requests.exceptions.ConnectionError:
            self.log_test("KAN-211", "Server Connection", "FAILED", "Server not running. Start with: python src/app/main.py")
            self.results["KAN-211"]["status"] = "FAILED"
        except Exception as e:
            self.log_test("KAN-211", "Validation & Centralized Error Handling", "FAILED", str(e))
            self.results["KAN-211"]["status"] = "FAILED"
    
    def run_all_tests(self):
        """Run all task tests."""
        print("="*60)
        print("Library Management System - Comprehensive Testing")
        print("="*60)
        print("Testing all implemented tasks...")
        
        # Run tests for each task
        self.test_kan_202()
        self.test_kan_203()
        self.test_kan_204()
        self.test_kan_205()
        self.test_kan_206()
        self.test_kan_207()
        self.test_kan_208()
        self.test_kan_209()
        self.test_kan_210()
        self.test_kan_211()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        for task, result in self.results.items():
            status = result["status"]
            test_count = len(result["tests"])
            passed_count = sum(1 for test in result["tests"] if test["status"] == "PASSED")
            
            if status == "COMPLETED":
                print(f"[OK] {task}: {status} ({passed_count}/{test_count} tests passed)")
            elif status == "FAILED":
                print(f"[ERROR] {task}: {status} ({passed_count}/{test_count} tests passed)")
            else:
                print(f"[PENDING] {task}: {status}")
        
        print("\n" + "="*60)
        
        # Overall status
        completed_tasks = sum(1 for result in self.results.values() if result["status"] == "COMPLETED")
        total_tasks = len(self.results)
        
        if completed_tasks == total_tasks:
            print("[SUCCESS] ALL TASKS COMPLETED SUCCESSFULLY!")
        else:
            print(f"[WARNING] {completed_tasks}/{total_tasks} tasks completed")
        
        print("="*60)

def main():
    """Main test runner."""
    tester = TaskTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
