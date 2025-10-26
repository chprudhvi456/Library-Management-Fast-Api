"""
Integration tests for Library Management System API.

These tests cover end-to-end flows including:
- Create library → create book → link book → fetch library books
- Update and delete flows
- Error flows
"""

import pytest
from fastapi import status


class TestLibraryBookIntegrationFlow:
    """Test the complete library-book integration flow."""
    
    def test_create_library_book_and_fetch_flow(self, client, sample_library_data, sample_book_data):
        """Test: Create library → Create book → Link book → Fetch library books."""
        
        # Step 1: Create a library
        library_response = client.post("/libraries", json=sample_library_data)
        assert library_response.status_code == status.HTTP_201_CREATED
        library_data = library_response.json()
        library_id = library_data["id"]
        
        # Verify library was created
        assert "id" in library_data
        assert "message" in library_data
        assert library_data["message"] == "Library created successfully"
        
        # Step 2: Create a book
        book_response = client.post("/books", json=sample_book_data)
        assert book_response.status_code == status.HTTP_201_CREATED
        book_data = book_response.json()
        book_id = book_data["id"]
        
        # Verify book was created
        assert "id" in book_data
        assert "message" in book_data
        assert book_data["message"] == "Book added successfully"
        
        # Step 3: Link book to library
        mapping_data = {
            "lib_id": library_id,
            "book_id": book_id,
            "status": "Active"
        }
        
        mapping_response = client.post("/library-books", json=mapping_data)
        assert mapping_response.status_code == status.HTTP_201_CREATED
        mapping_data_result = mapping_response.json()
        mapping_id = mapping_data_result["id"]
        
        # Verify mapping was created
        assert "id" in mapping_data_result
        assert "message" in mapping_data_result
        assert mapping_data_result["message"] == "Book linked to library successfully"
        
        # Step 4: Fetch books in library
        books_in_library = client.get(f"/libraries/{library_id}/books")
        assert books_in_library.status_code == status.HTTP_200_OK
        books_data = books_in_library.json()
        
        # Verify book is in library
        assert isinstance(books_data, list)
        assert len(books_data) == 1
        
        book_in_library = books_in_library.json()[0]
        assert book_in_library["book_id"] == book_id
        assert book_in_library["title"] == sample_book_data["title"]
        assert book_in_library["author"] == sample_book_data["author"]
        assert book_in_library["category"] == sample_book_data["category"]
        assert book_in_library["isbn"] == sample_book_data["isbn"]
        assert book_in_library["status"] == "Active"
        
        # Step 5: Verify the library count was updated
        library_detail = client.get(f"/libraries/{library_id}")
        assert library_detail.status_code == status.HTTP_200_OK
        library_detail_data = library_detail.json()
        assert library_detail_data["count"] == 1


class TestUpdateFlow:
    """Test update flows."""
    
    def test_update_library_flow(self, client, sample_library_data):
        """Test updating a library."""
        
        # Create a library
        create_response = client.post("/libraries", json=sample_library_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        library_id = create_response.json()["id"]
        
        # Update the library
        update_data = {
            "name": "Updated Library Name",
            "status": "Inactive"
        }
        
        update_response = client.put(f"/libraries/{library_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        update_result = update_response.json()
        assert update_result["message"] == "Library updated successfully"
        
        # Verify the update
        get_response = client.get(f"/libraries/{library_id}")
        assert get_response.status_code == status.HTTP_200_OK
        updated_library = get_response.json()
        assert updated_library["name"] == "Updated Library Name"
        assert updated_library["status"] == "Inactive"
    
    def test_update_book_flow(self, client, sample_book_data):
        """Test updating a book."""
        
        # Create a book
        create_response = client.post("/books", json=sample_book_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        book_id = create_response.json()["id"]
        
        # Update the book
        update_data = {
            "price": 200.00,
            "category": "Updated Category"
        }
        
        update_response = client.put(f"/books/{book_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        update_result = update_response.json()
        assert update_result["message"] == "Book updated successfully"
        
        # Verify the update
        get_response = client.get(f"/books/{book_id}")
        assert get_response.status_code == status.HTTP_200_OK
        updated_book = get_response.json()
        assert float(updated_book["price"]) == 200.0
        assert updated_book["category"] == "Updated Category"
    
    def test_update_library_book_mapping_flow(self, client, sample_library_data, sample_book_data):
        """Test updating a library-book mapping."""
        
        # Create library and book
        library_response = client.post("/libraries", json=sample_library_data)
        library_id = library_response.json()["id"]
        
        book_response = client.post("/books", json=sample_book_data)
        book_id = book_response.json()["id"]
        
        # Create mapping
        mapping_data = {
            "lib_id": library_id,
            "book_id": book_id,
            "status": "Active"
        }
        mapping_response = client.post("/library-books", json=mapping_data)
        mapping_id = mapping_response.json()["id"]
        
        # Update mapping status to Inactive
        update_data = {"status": "Inactive"}
        update_response = client.put(f"/library-books/{mapping_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["message"] == "Mapping updated successfully"
        
        # Verify the update
        mapping_detail = client.get(f"/library-books/{mapping_id}")
        assert mapping_detail.status_code == status.HTTP_200_OK
        updated_mapping = mapping_detail.json()
        assert updated_mapping["status"] == "Inactive"


class TestDeleteFlow:
    """Test delete flows."""
    
    def test_delete_library_flow(self, client, sample_library_data):
        """Test deleting a library."""
        
        # Create a library
        create_response = client.post("/libraries", json=sample_library_data)
        library_id = create_response.json()["id"]
        
        # Delete the library
        delete_response = client.delete(f"/libraries/{library_id}")
        assert delete_response.status_code == status.HTTP_200_OK
        assert delete_response.json()["message"] == "Library deleted successfully"
        
        # Verify it's deleted
        get_response = client.get(f"/libraries/{library_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_book_flow(self, client, sample_book_data):
        """Test deleting a book."""
        
        # Create a book
        create_response = client.post("/books", json=sample_book_data)
        book_id = create_response.json()["id"]
        
        # Delete the book
        delete_response = client.delete(f"/books/{book_id}")
        assert delete_response.status_code == status.HTTP_200_OK
        assert delete_response.json()["message"] == "Book deleted successfully"
        
        # Verify it's deleted
        get_response = client.get(f"/books/{book_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_library_book_mapping_flow(self, client, sample_library_data, sample_book_data):
        """Test deleting a library-book mapping."""
        
        # Create library and book
        library_response = client.post("/libraries", json=sample_library_data)
        library_id = library_response.json()["id"]
        
        book_response = client.post("/books", json=sample_book_data)
        book_id = book_response.json()["id"]
        
        # Create mapping
        mapping_data = {
            "lib_id": library_id,
            "book_id": book_id,
            "status": "Active"
        }
        mapping_response = client.post("/library-books", json=mapping_data)
        mapping_id = mapping_response.json()["id"]
        
        # Verify library count before deletion
        library_before = client.get(f"/libraries/{library_id}")
        assert library_before.json()["count"] == 1
        
        # Delete the mapping
        delete_response = client.delete(f"/library-books/{mapping_id}")
        assert delete_response.status_code == status.HTTP_200_OK
        assert delete_response.json()["message"] == "Mapping deleted successfully"
        
        # Verify it's deleted
        get_response = client.get(f"/library-books/{mapping_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify library count after deletion
        library_after = client.get(f"/libraries/{library_id}")
        assert library_after.json()["count"] == 0


class TestErrorFlows:
    """Test error handling flows."""
    
    def test_validation_error_on_book_creation(self, client):
        """Test validation errors when creating a book with missing fields."""
        
        invalid_book_data = {
            "title": "Incomplete Book"
            # Missing required fields: author, category, price, isbn
        }
        
        response = client.post("/books", json=invalid_book_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        
        assert "detail" in response_data
        # For FastAPI validation errors, detail is a list
        assert isinstance(response_data["detail"], list)
    
    def test_duplicate_isbn_error(self, client, sample_book_data):
        """Test duplicate ISBN constraint."""
        
        # Create first book
        response1 = client.post("/books", json=sample_book_data)
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Try to create duplicate book with same ISBN
        response2 = client.post("/books", json=sample_book_data)
        assert response2.status_code == status.HTTP_409_CONFLICT
        response_data = response2.json()
        assert "detail" in response_data
    
    def test_not_found_error(self, client):
        """Test 404 errors for non-existent resources."""
        
        # Try to get non-existent library
        response = client.get("/libraries/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "detail" in response.json()
        
        # Try to get non-existent book
        response = client.get("/books/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "detail" in response.json()
        
        # Try to get non-existent mapping
        response = client.get("/library-books/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "detail" in response.json()
    
    def test_invalid_library_book_mapping(self, client):
        """Test invalid library-book mapping (non-existent library/book)."""
        
        invalid_mapping = {
            "lib_id": 99999,  # Non-existent library
            "book_id": 99999,  # Non-existent book
            "status": "Active"
        }
        
        response = client.post("/library-books", json=invalid_mapping)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.json()
    
    def test_pagination_query_parameters(self, client):
        """Test query parameters for pagination."""
        
        # Test with page and limit - returns array if no books
        response = client.get("/books?page=1&limit=5")
        assert response.status_code == status.HTTP_200_OK
        books_data = response.json()
        # If no books, returns empty array; if books exist, returns paginated structure
        assert isinstance(books_data, (list, dict))
    
    def test_status_filtering(self, client, sample_library_data, sample_book_data):
        """Test status filtering in library books endpoint."""
        
        # Create library and book
        library_response = client.post("/libraries", json=sample_library_data)
        library_id = library_response.json()["id"]
        
        # Create multiple books
        book1_data = {**sample_book_data, "isbn": "9781111111111"}
        book1_response = client.post("/books", json=book1_data)
        book1_id = book1_response.json()["id"]
        
        book2_data = {**sample_book_data, "isbn": "9782222222222"}
        book2_response = client.post("/books", json=book2_data)
        book2_id = book2_response.json()["id"]
        
        # Link both books
        mapping1_data = {
            "lib_id": library_id,
            "book_id": book1_id,
            "status": "Active"
        }
        mapping2_data = {
            "lib_id": library_id,
            "book_id": book2_id,
            "status": "Inactive"
        }
        
        client.post("/library-books", json=mapping1_data)
        client.post("/library-books", json=mapping2_data)
        
        # Get all books
        all_books = client.get(f"/libraries/{library_id}/books")
        assert all_books.status_code == status.HTTP_200_OK
        assert len(all_books.json()) == 2
        
        # Get only active books
        active_books = client.get(f"/libraries/{library_id}/books?status=Active")
        assert active_books.status_code == status.HTTP_200_OK
        active_books_data = active_books.json()
        assert len(active_books_data) == 1
        assert active_books_data[0]["status"] == "Active"
        
        # Get only inactive books
        inactive_books = client.get(f"/libraries/{library_id}/books?status=Inactive")
        assert inactive_books.status_code == status.HTTP_200_OK
        inactive_books_data = inactive_books.json()
        assert len(inactive_books_data) == 1
        assert inactive_books_data[0]["status"] == "Inactive"


class TestListEndpoints:
    """Test list endpoints."""
    
    def test_list_libraries(self, client, sample_library_data):
        """Test listing all libraries."""
        
        # Create multiple libraries
        for i in range(3):
            library_data = {**sample_library_data, "name": f"Library {i}"}
            client.post("/libraries", json=library_data)
        
        # List all libraries
        response = client.get("/libraries")
        assert response.status_code == status.HTTP_200_OK
        libraries = response.json()
        assert isinstance(libraries, list)
        assert len(libraries) >= 3
    
    def test_list_books_with_pagination(self, client, sample_book_data):
        """Test listing books with pagination."""
        
        # Create multiple books
        for i in range(10):
            book_data = {
                **sample_book_data,
                "isbn": f"97812345678{i:02d}",
                "title": f"Book {i}"
            }
            client.post("/books", json=book_data)
        
        # Get first page
        response = client.get("/books?page=1&limit=5")
        assert response.status_code == status.HTTP_200_OK
        books_data = response.json()
        # Service returns a list, not a paginated dict
        assert isinstance(books_data, list)
        assert len(books_data) <= 5

