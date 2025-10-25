from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.application.payrollperiods.payroll_periods_dto import PayrollPeriodCreateDTO, PayrollPeriodUpdateDTO
from app.dependencies import get_payroll_period_service

router = APIRouter()

@router.get("/payroll-periods")
def get_all_payroll_periods(db: Session = Depends(get_db)):
    service = get_payroll_period_service(db)
    response = service.get_all_periods()
    return response

@router.post("/create-payroll-period")
def create_employee(dto: PayrollPeriodCreateDTO, db: Session = Depends(get_db)):
    service = get_payroll_period_service(db)
    response = service.create_payroll_period(dto)
    return response

@router.put("/update-payroll-period")
def update_employee(dto: PayrollPeriodUpdateDTO, db: Session = Depends(get_db)):
    service = get_payroll_period_service(db)
    response = service.update_payroll_period(dto)
    return response