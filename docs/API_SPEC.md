# Library Book Management System - API Specification

## Overview

This document provides a comprehensive specification for the Library Book Management System API. The API is built with FastAPI and provides RESTful endpoints for managing libraries, books, and their relationships.

**Base URL**: `http://localhost:8000/api/v1`

## Authentication

Currently, the API does not require authentication. Future versions may include API key authentication.

## Data Models

### Library
- **id**: `INT PRIMARY KEY AUTO_INCREMENT`
- **name**: `VARCHAR(255) NOT NULL`
- **dept**: `VARCHAR(100) NULL`
- **count**: `INT DEFAULT 0`
- **status**: `ENUM('Active','Inactive') DEFAULT 'Active'`
- **created_at**: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- **updated_at**: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`

### Book
- **id**: `INT PRIMARY KEY AUTO_INCREMENT`
- **title**: `VARCHAR(255) NOT NULL`
- **author**: `VARCHAR(255) NOT NULL`
- **category**: `VARCHAR(100) NULL`
- **price**: `DECIMAL(10,2) NOT NULL`
- **isbn**: `VARCHAR(20) NOT NULL UNIQUE`
- **created_at**: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- **updated_at**: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`

### Library_Book
- **id**: `INT PRIMARY KEY AUTO_INCREMENT`
- **lib_id**: `INT NOT NULL` (FK to libraries.id)
- **book_id**: `INT NOT NULL` (FK to books.id)
- **status**: `ENUM('Active','Inactive') DEFAULT 'Active'`
- **created_at**: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- **updated_at**: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`
- **UNIQUE(lib_id, book_id)**

## API Endpoints

### Libraries

#### POST /api/v1/libraries
Create a new library.

**Request Body:**
```json
{
  "name": "Main Library",
  "dept": "CSE",
  "count": 200,
  "status": "Active"
}
```

**Validation Rules:**
- `name`: Required, string, max 255 characters
- `dept`: Optional, string, max 100 characters
- `count`: Optional, integer, default 0, minimum 0
- `status`: Optional, enum ['Active', 'Inactive'], default 'Active'

**Response (201 Created):**
```json
{
  "id": 1,
  "message": "Library created successfully"
}
```

**Response (422 Validation Error):**
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### GET /api/v1/libraries
List all libraries with optional pagination.

**Query Parameters:**
- `page`: Optional, integer, default 1, minimum 1
- `limit`: Optional, integer, default 10, minimum 1, maximum 100
- `status`: Optional, string, filter by status ['Active', 'Inactive']

**Response (200 OK):**
```json
{
  "libraries": [
    {
      "id": 1,
      "name": "Main Library",
      "dept": "CSE",
      "count": 200,
      "status": "Active",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

#### GET /api/v1/libraries/{id}
Get a specific library by ID.

**Path Parameters:**
- `id`: Required, integer, library ID

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Main Library",
  "dept": "CSE",
  "count": 200,
  "status": "Active",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Library not found"
}
```

#### PUT /api/v1/libraries/{id}
Update a library (partial update allowed).

**Path Parameters:**
- `id`: Required, integer, library ID

**Request Body:**
```json
{
  "name": "Updated Library Name",
  "dept": "Updated Dept",
  "count": 250,
  "status": "Inactive"
}
```

**Validation Rules:**
- All fields optional for partial update
- Same validation rules as POST

**Response (200 OK):**
```json
{
  "id": 1,
  "message": "Library updated successfully"
}
```

#### DELETE /api/v1/libraries/{id}
Delete a library.

**Path Parameters:**
- `id`: Required, integer, library ID

**Response (200 OK):**
```json
{
  "message": "Library deleted successfully"
}
```

**Response (409 Conflict):**
```json
{
  "detail": "Cannot delete library with active book mappings"
}
```

### Books

#### POST /api/v1/books
Create a new book.

**Request Body:**
```json
{
  "title": "AI Fundamentals",
  "author": "John Smith",
  "category": "AI",
  "price": 550.00,
  "isbn": "9781234567890"
}
```

**Validation Rules:**
- `title`: Required, string, max 255 characters
- `author`: Required, string, max 255 characters
- `category`: Optional, string, max 100 characters
- `price`: Required, decimal, minimum 0.01, maximum 999999.99
- `isbn`: Required, string, max 20 characters, unique

**Response (201 Created):**
```json
{
  "id": 101,
  "message": "Book added successfully"
}
```

**Response (409 Conflict):**
```json
{
  "detail": "Conflict: ISBN already exists",
  "errors": [
    {
      "field": "isbn",
      "message": "A book with this ISBN already exists."
    }
  ]
}
```

#### GET /api/v1/books
List all books with optional pagination and filtering.

**Query Parameters:**
- `page`: Optional, integer, default 1, minimum 1
- `limit`: Optional, integer, default 10, minimum 1, maximum 100
- `category`: Optional, string, filter by category
- `author`: Optional, string, filter by author
- `search`: Optional, string, search in title and author

**Response (200 OK):**
```json
{
  "books": [
    {
      "id": 101,
      "title": "AI Fundamentals",
      "author": "John Smith",
      "category": "AI",
      "price": 550.00,
      "isbn": "9781234567890",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

#### GET /api/v1/books/{id}
Get a specific book by ID.

**Path Parameters:**
- `id`: Required, integer, book ID

**Response (200 OK):**
```json
{
  "id": 101,
  "title": "AI Fundamentals",
  "author": "John Smith",
  "category": "AI",
  "price": 550.00,
  "isbn": "9781234567890",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### PUT /api/v1/books/{id}
Update a book (partial update allowed).

**Path Parameters:**
- `id`: Required, integer, book ID

**Request Body:**
```json
{
  "title": "Updated Book Title",
  "author": "Updated Author",
  "category": "Updated Category",
  "price": 600.00,
  "isbn": "9781234567891"
}
```

**Validation Rules:**
- All fields optional for partial update
- Same validation rules as POST
- ISBN must be unique if provided

**Response (200 OK):**
```json
{
  "id": 101,
  "message": "Book updated successfully"
}
```

#### DELETE /api/v1/books/{id}
Delete a book.

**Path Parameters:**
- `id`: Required, integer, book ID

**Response (200 OK):**
```json
{
  "message": "Book deleted successfully"
}
```

**Response (409 Conflict):**
```json
{
  "detail": "Cannot delete book with active library mappings"
}
```

### Library-Book Mappings

#### POST /api/v1/library-books
Link a book to a library.

**Request Body:**
```json
{
  "lib_id": 1,
  "book_id": 101,
  "status": "Active"
}
```

**Validation Rules:**
- `lib_id`: Required, integer, must exist in libraries table
- `book_id`: Required, integer, must exist in books table
- `status`: Optional, enum ['Active', 'Inactive'], default 'Active'

**Response (201 Created):**
```json
{
  "id": 501,
  "message": "Book linked to library successfully"
}
```

**Response (409 Conflict):**
```json
{
  "detail": "Book is already linked to this library"
}
```

#### GET /api/v1/library-books
List all library-book mappings with optional pagination.

**Query Parameters:**
- `page`: Optional, integer, default 1, minimum 1
- `limit`: Optional, integer, default 10, minimum 1, maximum 100
- `lib_id`: Optional, integer, filter by library ID
- `book_id`: Optional, integer, filter by book ID
- `status`: Optional, string, filter by status ['Active', 'Inactive']

**Response (200 OK):**
```json
{
  "mappings": [
    {
      "id": 501,
      "lib_id": 1,
      "book_id": 101,
      "status": "Active",
      "library": {
        "id": 1,
        "name": "Main Library",
        "dept": "CSE"
      },
      "book": {
        "id": 101,
        "title": "AI Fundamentals",
        "author": "John Smith",
        "isbn": "9781234567890"
      },
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

#### GET /api/v1/library-books/{id}
Get a specific library-book mapping by ID.

**Path Parameters:**
- `id`: Required, integer, mapping ID

**Response (200 OK):**
```json
{
  "id": 501,
  "lib_id": 1,
  "book_id": 101,
  "status": "Active",
  "library": {
    "id": 1,
    "name": "Main Library",
    "dept": "CSE"
  },
  "book": {
    "id": 101,
    "title": "AI Fundamentals",
    "author": "John Smith",
    "isbn": "9781234567890"
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### PUT /api/v1/library-books/{id}
Update a library-book mapping status.

**Path Parameters:**
- `id`: Required, integer, mapping ID

**Request Body:**
```json
{
  "status": "Inactive"
}
```

**Validation Rules:**
- `status`: Required, enum ['Active', 'Inactive']

**Response (200 OK):**
```json
{
  "id": 501,
  "message": "Mapping updated successfully"
}
```

#### DELETE /api/v1/library-books/{id}
Delete a library-book mapping.

**Path Parameters:**
- `id`: Required, integer, mapping ID

**Response (200 OK):**
```json
{
  "message": "Mapping deleted successfully"
}
```

### Joined Queries

#### GET /api/v1/libraries/{id}/books
List all books in a specific library with book metadata.

**Path Parameters:**
- `id`: Required, integer, library ID

**Query Parameters:**
- `page`: Optional, integer, default 1, minimum 1
- `limit`: Optional, integer, default 10, minimum 1, maximum 100
- `status`: Optional, string, filter by mapping status ['Active', 'Inactive']

**Response (200 OK):**
```json
{
  "library": {
    "id": 1,
    "name": "Main Library",
    "dept": "CSE",
    "count": 200
  },
  "books": [
    {
      "book_id": 101,
      "title": "AI Fundamentals",
      "author": "John Smith",
      "category": "AI",
      "price": 550.00,
      "isbn": "9781234567890",
      "status": "Active",
      "mapping_id": 501,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

## Error Responses

### Standard Error Format
```json
{
  "detail": "Error message",
  "errors": [
    {
      "field": "field_name",
      "message": "Specific field error message"
    }
  ]
}
```

### HTTP Status Codes
- **200 OK**: Successful GET, PUT, DELETE
- **201 Created**: Successful POST
- **400 Bad Request**: Invalid request data
- **404 Not Found**: Resource not found
- **409 Conflict**: Business logic violation (duplicate ISBN, etc.)
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error

## Environment Variables

### Required Environment Variables
```bash
# Database Configuration
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/library_db
MYSQL_USER=library_user
MYSQL_PASSWORD=library_password
MYSQL_DB=library_db
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Application Configuration
APP_NAME=Library Management System
APP_VERSION=1.0.0
DEBUG=True
LOG_LEVEL=INFO

# Security (Optional)
SECRET_KEY=your-secret-key-here
API_KEY=your-api-key-here
```

### Docker Compose Configuration
```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: library_db
      MYSQL_USER: library_user
      MYSQL_PASSWORD: library_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql+pymysql://library_user:library_password@mysql:3306/library_db
    depends_on:
      - mysql

volumes:
  mysql_data:
```

## Local Development Setup

1. **Prerequisites:**
   - Python 3.11+
   - Docker and Docker Compose
   - Git

2. **Setup:**
   ```bash
   # Clone repository
   git clone <repository-url>
   cd library_management
   
   # Copy environment file
   cp .env.example .env
   
   # Start services
   docker-compose up -d mysql
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   alembic upgrade head
   
   # Start application
   uvicorn src.app.main:app --reload
   ```

3. **Access API Documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Testing

### Test Coverage Requirements
- Unit tests: ≥70% coverage for core logic
- Integration tests: All endpoints tested
- Database tests: CRUD operations and constraints

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_libraries.py -v
```

## Performance Considerations

### Database Indexes
```sql
-- Libraries table indexes
CREATE INDEX idx_libraries_status ON libraries(status);
CREATE INDEX idx_libraries_dept ON libraries(dept);

-- Books table indexes
CREATE INDEX idx_books_isbn ON books(isbn);
CREATE INDEX idx_books_category ON books(category);
CREATE INDEX idx_books_author ON books(author);
CREATE INDEX idx_books_title ON books(title);

-- Library_books table indexes
CREATE INDEX idx_library_books_lib_id ON library_books(lib_id);
CREATE INDEX idx_library_books_book_id ON library_books(book_id);
CREATE INDEX idx_library_books_status ON library_books(status);
CREATE INDEX idx_library_books_lib_book ON library_books(lib_id, book_id);
```

### Pagination
- Default page size: 10 items
- Maximum page size: 100 items
- All list endpoints support pagination

### Query Optimization
- Use JOIN queries instead of N+1 queries
- Implement proper database indexes
- Use database transactions for complex operations

## Security Considerations

### Input Validation
- All inputs validated using Pydantic models
- SQL injection prevention through SQLAlchemy ORM
- XSS prevention through proper response formatting

### CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting (Future Enhancement)
- Consider implementing rate limiting for production
- Use slowapi or similar for rate limiting
- Configure appropriate limits per endpoint

## Monitoring and Logging

### Structured Logging
```python
import logging
import json

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Health Check Endpoint
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## API Versioning

- Current version: v1
- Version included in all endpoint paths: `/api/v1/`
- Future versions will maintain backward compatibility
- Deprecated endpoints will be marked and removed in future versions

## Support and Documentation

- **API Documentation**: Available at `/docs` (Swagger UI) and `/redoc`
- **OpenAPI Schema**: Available at `/openapi.json`
- **Health Check**: Available at `/health`
- **Repository**: [GitHub Repository URL]
- **Issues**: [GitHub Issues URL]
