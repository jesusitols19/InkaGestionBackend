# app/infrastructure/scheduled_report_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, Boolean, func, text
from datetime import datetime, timedelta
from app.infrastructure.database import Base
from app.domain.scheduledreports import ScheduledReport
from app.helpers.orm_mapper import to_model, to_entity

class ScheduledReportModel(Base):
    __tablename__ = "scheduled_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    frequency = Column(Enum('DAILY', 'WEEKLY', 'MONTHLY', 'MANUAL'), default='MANUAL')
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    recipients = Column(Text, nullable=True)
    template = Column(String(255), nullable=True)
    active = Column(Boolean, default=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())


class ScheduledReportRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):

        reports = self.db.query(ScheduledReportModel).all()

        return [to_entity(report, ScheduledReport) for report in reports]
        

    def create_report(self, scheduledReport: ScheduledReport):
        model = to_model(scheduledReport,ScheduledReportModel)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return to_entity(model,ScheduledReport)
    
    def update_report(self, scheduledReport: ScheduledReport):

        
        existing_report = self.db.query(ScheduledReportModel).filter(ScheduledReportModel.id == scheduledReport.id).first()
    
        if not existing_report:
            return "No existe un reporte con ese id"
        
        for key, value in scheduledReport.__dict__.items():
            setattr(existing_report, key, value)

        self.db.commit()
        self.db.refresh(existing_report)

        return "Si se pudo hacer"

        # return to_entity(existing_report,ScheduledReport)


    def get_due_reports(self):
        
        now = datetime.now()

        reports = self.db.query(ScheduledReportModel).filter(ScheduledReportModel.active == True).filter(ScheduledReportModel.next_run <= now).all()

        return [to_entity(report, ScheduledReport) for report in reports]
    
    def update_run_dates(self, scheduledReport: ScheduledReport):

        existing_report = self.db.query(ScheduledReportModel).filter(ScheduledReportModel.id == scheduledReport.id).first()

        now = datetime.now()

        scheduledReport.last_run = now

        if scheduledReport.frequency == 'DAILY':
            scheduledReport.next_run = now + timedelta(days=1)
        elif scheduledReport.frequency == 'WEEKLY':
            scheduledReport.next_run = now + timedelta(weeks=1)
        elif scheduledReport.frequency == 'MONTHLY':
            scheduledReport.next_run = now + timedelta(days=30)

        for key, value in scheduledReport.__dict__.items():
            setattr(existing_report, key, value)
        
        self.db.commit()
        self.db.refresh(existing_report)

    def get_mysql_views(self):
        sql = text("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        result = self.db.execute(sql)
        rows = result.fetchall()
        
        # Convierte las tuplas en diccionarios legibles
        views = []
        for row in rows:
            # row.keys() devuelve los nombres de columnas
            view_name = row[0]
            view_type = row[1]
            views.append({
                "name": view_name,
                "type": view_type
            })
        return views
