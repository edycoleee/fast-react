from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.modules.access.service import AccessService
from backend.app.modules.auth.dependencies import require_permission

router = APIRouter(prefix="/access", tags=["access"])


@router.get("/summary")
def get_access_summary(
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("access.read")),
) -> dict:
    summary = AccessService(db).summary()
    return {
        "success": True,
        "message": "Access summary fetched",
        "data": summary,
        "meta": None,
    }
