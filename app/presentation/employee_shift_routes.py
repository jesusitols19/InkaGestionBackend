from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.dependencies import get_employee_shift_service
from app.application.employeeshift.employee_shift_dto import EmployeeShiftCreateDTO

router = APIRouter()

@router.post("/create-employee-shift")
def create_employee_shift(dto: EmployeeShiftCreateDTO, db: Session = Depends(get_db)):
    service = get_employee_shift_service(db)
    response = service.create_employee_shift(dto)
    return response

@router.get("/get-all-employee-shift")
def get_all_shift(db: Session = Depends(get_db)):
    service = get_employee_shift_service(db)
    response = service.get_all_employee_shift()
    return response
