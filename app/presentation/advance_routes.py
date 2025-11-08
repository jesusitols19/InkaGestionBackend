from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.dependencies import get_advance_service
from app.application.advance.advance_dto import AdvanceRequestDTO, AdvanceApproveDTO


router = APIRouter()

@router.get("/get-all-advances")
def get_all_advances(db: Session = Depends(get_db)):
    service = get_advance_service(db)
    response = service.get_all_advances()
    return response


@router.post("/request-advance")
def request_advance(dto: AdvanceRequestDTO, db: Session = Depends(get_db)):
    service = get_advance_service(db)
    response = service.request_advance(dto)
    return response


@router.put("/approve-advance")
def approve_advance(dto: AdvanceApproveDTO, db: Session = Depends(get_db)):
    service = get_advance_service(db)
    response = service.approve_advance(dto)
    return response


@router.put("/mark-paid/{advance_id}")
def mark_paid(advance_id:int, db: Session = Depends(get_db)):
    service = get_advance_service(db)
    response = service.mark_paid(advance_id)
    return response