from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.dependencies import get_dashboard_service

router = APIRouter()


@router.get("/get-full-dashboard")
def get_full_dashboard(db: Session = Depends(get_db)):
    service = get_dashboard_service(db)
    response = service.get_full_dashboard()
    return response