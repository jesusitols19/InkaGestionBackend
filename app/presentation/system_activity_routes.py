from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.application.systemactivity.system_activity_dto import SystemActivityCreateDTO
from app.dependencies import get_system_activity_service

router = APIRouter()


@router.get("/list-system-activities")
def list_system_activities(db: Session = Depends(get_db)):
    service = get_system_activity_service(db)
    response = service.get_all()
    return response


@router.post("/add-system-activity")
def add_system_activities(dto: SystemActivityCreateDTO, db: Session = Depends(get_db)):
    service = get_system_activity_service(db)
    response = service.add_system_activity(dto)
    return response