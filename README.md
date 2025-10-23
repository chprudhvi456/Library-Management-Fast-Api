# Library Book Management System

A production-ready RESTful Library Book Management API built with FastAPI, SQLAlchemy, and MySQL.

## Project Structure

```
library_management/
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── library.py
│   │   │   ├── book.py
│   │   │   └── library_book.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── library.py
│   │   │   ├── book.py
│   │   │   └── library_book.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── libraries.py
│   │   │   ├── books.py
│   │   │   └── library_books.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── library_service.py
│   │   │   ├── book_service.py
│   │   │   └── library_book_service.py
│   │   └── crud/
│   │       ├── __init__.py
│   │       ├── library_crud.py
│   │       ├── book_crud.py
│   │       └── library_book_crud.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_libraries.py
│   ├── test_books.py
│   └── test_library_books.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
├── docs/
│   ├── API_SPEC.md
│   └── SETUP.md
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd library_management
   cp .env.example .env
   ```

2. **Start with Docker:**
   ```bash
   docker-compose up -d
   ```

3. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Start the application:**
   ```bash
   uvicorn src.app.main:app --reload
   ```

5. **Access API docs:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Environment Variables

See `.env.example` for required environment variables.

## API Documentation

Complete API specification available in [docs/API_SPEC.md](docs/API_SPEC.md)

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_libraries.py
```

## Development

- **Database**: MySQL 8.x
- **ORM**: SQLAlchemy with Alembic migrations
- **API**: FastAPI with automatic OpenAPI documentation
- **Testing**: pytest with httpx TestClient
- **Containerization**: Docker & docker-compose
