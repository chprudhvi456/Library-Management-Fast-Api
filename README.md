# Library Management System

A production-ready RESTful Library Management API built with FastAPI, SQLAlchemy, and MySQL. This system provides comprehensive CRUD operations for libraries, books, and their relationships.

## 🎯 **Implemented Features**

### **✅ KAN-202: Database Setup & Models**
- SQLAlchemy ORM models for Library, Book, and LibraryBook
- Database relationships and constraints
- Alembic migrations support

### **✅ KAN-203: SQLAlchemy Models & Pydantic Schemas**
- Complete Pydantic schemas for request/response validation
- CRUD operations for all entities
- Comprehensive data validation

### **✅ KAN-204: Library CRUD Endpoints**
- POST /libraries - Create new libraries
- GET /libraries - List all libraries
- Clean JSON response format
- Proper validation and error handling

## 📁 **Project Structure**

```
Library_Management/
├── src/
│   └── app/
│       ├── main.py                 # FastAPI application
│       ├── database.py            # Database configuration
│       ├── models/                 # SQLAlchemy models
│       │   ├── library.py
│       │   ├── book.py
│       │   └── library_book.py
│       ├── schemas/               # Pydantic schemas
│       │   ├── library.py
│       │   ├── book.py
│       │   └── library_book.py
│       └── crud/                  # CRUD operations
│           ├── library.py
│           ├── book.py
│           └── library_book.py
├── tests/
│   └── test_models_schemas.py    # Unit tests
├── docs/                         # Documentation
│   ├── KAN-202_COMPLETION_PROOF.md
│   ├── KAN-203_COMPLETION_PROOF.md
│   └── KAN-204_COMPLETION_PROOF.md
├── alembic/                      # Database migrations
├── test_all_tasks.py             # Comprehensive test suite
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.11+
- MySQL 8.x (or Docker)
- Git

### **1. Clone and Setup**
```bash
# Clone the repository
git clone <repository-url>
cd Library_Management

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Database Setup**

#### **Option A: Using Docker (Recommended)**
```bash
# Start MySQL with Docker
docker-compose up -d

# The database will be available at:
# Host: localhost
# Port: 3306
# Database: library_db
# Username: library_user
# Password: library_password
```

#### **Option B: Local MySQL Installation**
```bash
# Create database
mysql -u root -p
CREATE DATABASE library_db;
CREATE USER 'library_user'@'localhost' IDENTIFIED BY 'library_password';
GRANT ALL PRIVILEGES ON library_db.* TO 'library_user'@'localhost';
FLUSH PRIVILEGES;
```

### **3. Run Database Migrations**
```bash
# Run Alembic migrations
alembic upgrade head
```

### **4. Start the Application**
```bash
# Start the FastAPI server
python src/app/main.py

# Or using uvicorn directly
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
```

### **5. Access the API**
- **API Base URL**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/`

## 🧪 **Testing**

### **Run All Tests**
```bash
# Run comprehensive test suite
python test_all_tasks.py
```

### **Run Unit Tests**
```bash
# Run specific unit tests
python -m pytest tests/test_models_schemas.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### **Test Results**
```
[SUCCESS] ALL TASKS COMPLETED SUCCESSFULLY!
[OK] KAN-202: COMPLETED (4/4 tests passed)
[OK] KAN-203: COMPLETED (6/6 tests passed)
[OK] KAN-204: COMPLETED (5/5 tests passed)
```

## 📚 **API Endpoints**

### **Library Endpoints (KAN-204)**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/libraries` | Create a new library |
| GET | `/libraries` | Get all libraries |

### **Example Usage**

#### **Create Library**
```bash
curl -X POST "http://localhost:8000/libraries" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Main Library",
    "dept": "CSE",
    "count": 200,
    "status": "Active"
  }'
```

**Response:**
```json
{
  "id": 1,
  "message": "Library created successfully"
}
```

#### **Get All Libraries**
```bash
curl -X GET "http://localhost:8000/libraries"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Main Library",
    "dept": "CSE",
    "count": 200,
    "status": "Active"
  }
]
```

## 🔧 **Postman Testing**

### **Import Postman Collection**
1. Open Postman
2. Import the collection from `docs/KAN-204_COMPLETION_PROOF.md`
3. Set environment variables:
   - `base_url`: `http://localhost:8000`
4. Run the collection tests

### **Environment Variables**
```json
{
  "base_url": "http://localhost:8000"
}
```

## 📖 **Documentation**

- **[KAN-202 Documentation](docs/KAN-202_COMPLETION_PROOF.md)** - Database setup and models
- **[KAN-203 Documentation](docs/KAN-203_COMPLETION_PROOF.md)** - SQLAlchemy models and Pydantic schemas
- **[KAN-204 Documentation](docs/KAN-204_COMPLETION_PROOF.md)** - Library CRUD endpoints with Postman testing

## 🛠 **Development**

### **Tech Stack**
- **Backend**: FastAPI
- **Database**: MySQL 8.x
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Testing**: pytest
- **Containerization**: Docker

### **Project Features**
- ✅ **Clean Architecture**: Separation of concerns with models, schemas, and CRUD
- ✅ **Data Validation**: Comprehensive input validation with Pydantic
- ✅ **Database Relationships**: Proper foreign key relationships
- ✅ **Error Handling**: Proper HTTP status codes and error messages
- ✅ **API Documentation**: Auto-generated OpenAPI/Swagger docs
- ✅ **Testing**: Comprehensive unit and integration tests
- ✅ **Clean JSON Responses**: Simple, readable API responses

### **Code Quality**
- **Type Safety**: Full typing support throughout
- **Validation**: Input validation for all endpoints
- **Error Handling**: Proper exception handling
- **Documentation**: Comprehensive inline documentation
- **Testing**: High test coverage with multiple test types

## 🚀 **Production Deployment**

### **Docker Deployment**
```bash
# Build the image
docker build -t library-management .

# Run the container
docker run -p 8000:8000 library-management
```

### **Environment Variables**
```bash
# Database configuration
DATABASE_URL=mysql+pymysql://library_user:library_password@localhost:3306/library_db

# Application settings
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

## 📊 **Project Status**

| Task | Status | Tests | Documentation |
|------|--------|-------|---------------|
| KAN-202 | ✅ COMPLETED | 4/4 passed | ✅ Complete |
| KAN-203 | ✅ COMPLETED | 6/6 passed | ✅ Complete |
| KAN-204 | ✅ COMPLETED | 5/5 passed | ✅ Complete |

**Overall Status**: 🎉 **ALL TASKS COMPLETED SUCCESSFULLY!**
