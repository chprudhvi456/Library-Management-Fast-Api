"""
Centralized Exception Handlers for FastAPI

This module provides custom exception handlers for:
- HTTPException
- IntegrityError (SQLAlchemy)
- RequestValidationError (Pydantic)
"""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from pymysql.err import IntegrityError as PyMySQLIntegrityError
from typing import Dict, Any


def get_error_response(detail: str, errors: list = None) -> Dict[str, Any]:
    """
    Standardize error response format.
    
    Args:
        detail: Main error message
        errors: List of field-specific errors (optional)
        
    Returns:
        Standardized error response dictionary
    """
    response = {
        "detail": detail,
    }
    
    if errors:
        response["errors"] = errors
    
    return response


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle HTTPException errors.
    
    Returns standardized error response for HTTP exceptions.
    """
    detail = str(exc.detail) if hasattr(exc, 'detail') else "An error occurred"
    status_code = exc.status_code if hasattr(exc, 'status_code') else 500
    
    return JSONResponse(
        status_code=status_code,
        content=get_error_response(detail=detail)
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle Pydantic RequestValidationError.
    
    Returns standardized error response with field-level validation errors.
    """
    errors = []
    
    # Extract field-specific errors from Pydantic validation
    for error in exc.errors():
        field_path = " -> ".join(str(loc) for loc in error.get("loc", []))
        field_name = field_path if field_path else "unknown"
        error_msg = error.get("msg", "Validation error")
        error_type = error.get("type", "validation_error")
        
        errors.append({
            "field": field_name,
            "message": error_msg,
            "type": error_type
        })
    
    detail = "Validation error" if not errors else errors[0].get("message", "Validation error")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=get_error_response(detail=detail, errors=errors)
    )


async def integrity_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle SQLAlchemy IntegrityError and PyMySQL IntegrityError.
    
    Maps unique constraint violations to 409 Conflict.
    Maps foreign key constraint violations to 400 Bad Request.
    """
    error_message = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    
    # Check for unique constraint violation
    if "Duplicate entry" in error_message or "unique constraint" in error_message.lower():
        # Extract field name if possible
        field = "unknown"
        if "for key" in error_message:
            try:
                # Parse error like: (1062, "Duplicate entry 'value' for key 'table.field'")
                parts = error_message.split("for key '")
                if len(parts) > 1:
                    field = parts[1].split("'")[0]
            except:
                pass
        
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=get_error_response(
                detail="Duplicate entry - this record already exists",
                errors=[{
                    "field": field,
                    "message": "This value already exists and must be unique",
                    "type": "unique_constraint_violation"
                }]
            )
        )
    
    # Check for foreign key constraint violation
    elif "foreign key constraint" in error_message.lower() or "Cannot add or update a child row" in error_message:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=get_error_response(
                detail="Referenced record does not exist",
                errors=[{
                    "field": "foreign_key",
                    "message": "The referenced record does not exist",
                    "type": "foreign_key_constraint_violation"
                }]
            )
        )
    
    # Generic integrity error
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=get_error_response(detail="Database integrity constraint violation")
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle general exceptions.
    
    Returns standardized error response for unexpected errors.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=get_error_response(detail="An unexpected error occurred")
    )


def register_exception_handlers(app):
    """
    Register all custom exception handlers with the FastAPI app.
    
    Args:
        app: FastAPI application instance
    """
    # Register Pydantic validation error handler
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    
    # Register HTTP exception handler
    from fastapi import HTTPException
    app.add_exception_handler(HTTPException, http_exception_handler)
    
    # Register SQLAlchemy IntegrityError handler
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    
    # Register PyMySQL IntegrityError handler
    app.add_exception_handler(PyMySQLIntegrityError, integrity_error_handler)
    
    # Register general exception handler (should be last)
    app.add_exception_handler(Exception, general_exception_handler)

