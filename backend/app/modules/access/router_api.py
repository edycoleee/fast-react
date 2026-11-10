from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.modules.access.service import AccessService

router = APIRouter(prefix="/access", tags=["access"])


@router.get("/summary")
def get_access_summary(db: Session = Depends(get_db)) -> dict:
    summary = AccessService(db).summary()
    return {
        "success": True,
        "message": "Access summary fetched",
        "data": summary,
        "meta": None,
    }

