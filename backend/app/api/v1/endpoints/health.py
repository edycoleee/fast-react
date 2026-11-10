from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.core.database import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {
        "success": True,
        "message": "Application is healthy",
        "data": {"status": "ok"},
        "meta": None,
    }


@router.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "success": True,
            "message": "Database connection is healthy",
            "data": {"status": "ok"},
            "meta": None,
        }
    except SQLAlchemyError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "success": False,
                "message": "Database connection failed",
                "error": {"code": "db_unavailable"},
                "meta": None,
            },
        )
