"""
Pytest configuration and fixtures for integration tests.

This module provides test fixtures for database setup and FastAPI test client.
"""

import pytest
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add src to Python path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from app.database import get_db, Base
from app.main import app
from fastapi.testclient import TestClient


# Test database URL - using in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///./test_library.db"


@pytest.fixture(scope="function")
def test_db():
    """
    Create a test database session.
    
    Creates a new database for each test function and cleans up afterwards.
    """
    # Create test database engine
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    
    # Create test session
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """
    Create a test client for the FastAPI application.
    
    Overrides the database dependency to use the test database.
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sample_library_data():
    """Sample library data for testing."""
    return {
        "name": "Test Library",
        "dept": "CSE",
        "count": 0,
        "status": "Active"
    }


@pytest.fixture(scope="function")
def sample_book_data():
    """Sample book data for testing."""
    return {
        "title": "Test Book",
        "author": "Test Author",
        "category": "Test Category",
        "price": 100.00,
        "isbn": "9781234567890"
    }


@pytest.fixture(scope="function")
def sample_library_book_data():
    """Sample library-book mapping data for testing."""
    return {
        "status": "Active"
    }

