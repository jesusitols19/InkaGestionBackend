from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.dependencies import get_shift_service
from app.application.shift.shift_dto import ShiftCreateDTO


router = APIRouter()
@router.post("/create-shift")
def create_shift(dto: ShiftCreateDTO, db: Session = Depends(get_db)):
    service = get_shift_service(db)
    response = service.create_shift(dto)
    return response


@router.get("/get-all-shift")
def get_all_shift(db: Session = Depends(get_db)):
    service = get_shift_service(db)
    response = service.get_all_shift()
    return response