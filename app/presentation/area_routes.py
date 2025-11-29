from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.dependencies import get_area_service

router = APIRouter()

@router.get("/list-areas")
def list_areas(db: Session = Depends(get_db)):
    service = get_area_service(db)
    return service.get_all_areas()