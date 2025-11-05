# app/presentation/scheduled_report_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.dependencies import get_scheduled_report_service
from app.application.scheduledreport.scheduled_reports_dto import ScheduledReportCreateDTO, ScheduledReportUpdateDTO
# from app.application.scheduledreport.scheduled_report_dto import ScheduledReportCreateDTO

router = APIRouter()

@router.get("/get-all-reports")
def get_all_scheduled_reports(db: Session = Depends(get_db)):
    service = get_scheduled_report_service(db)
    return service.get_all()


@router.post("/create-scheduled-report")
def create_scheduled_report(dto: ScheduledReportCreateDTO, db: Session = Depends(get_db)):
    service = get_scheduled_report_service(db)
    return service.create_report(dto)


@router.put("/update-scheduled-report")
def create_scheduled_report(dto: ScheduledReportUpdateDTO, db: Session = Depends(get_db)):
    service = get_scheduled_report_service(db)
    return service.update_report(dto)

@router.post("/execute-manual")
def execute_reports_now(db: Session = Depends(get_db)):
    service = get_scheduled_report_service(db)
    return service.execute_due_reports()

@router.get("/get-mysql-views")
def get_mysql_views(db: Session = Depends(get_db)):
    service = get_scheduled_report_service(db)
    return service.get_mysql_views()
