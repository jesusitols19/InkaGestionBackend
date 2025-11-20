from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.dependencies import get_payroll_service
from app.application.payroll.payroll_dto import PayrollCreateDTO

router = APIRouter()

@router.get("/list-payrolls")
def list_payrolls(db: Session = Depends(get_db)):
    service = get_payroll_service(db)
    response = service.get_all_payrolls()
    return response

@router.post("/generate-payroll")
def generate_payroll(dto: PayrollCreateDTO, db: Session = Depends(get_db)):
    service = get_payroll_service(db)
    response = service.generate_payroll(dto)
    return response

@router.post("/export-excel-payroll/{planillaId}")
def export_excel_payroll(planillaId: int, db: Session = Depends(get_db)):
    service = get_payroll_service(db)
    response = service.export_payroll_to_excel(planillaId)
    return response

@router.post("/export-pdf-payroll/{planillaId}")
def export_pdf_payroll(planillaId: int, db: Session = Depends(get_db)):
    service = get_payroll_service(db)
    return service.export_payroll_to_pdf(planillaId)