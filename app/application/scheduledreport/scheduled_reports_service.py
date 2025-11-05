# app/application/scheduledreport/scheduled_report_service.py
from datetime import datetime
import pandas as pd
import os
from fastapi_mail import FastMail, MessageSchema, MessageType
from app.shared.mail_config import conf
from app.infrastructure.scheduled_reports_repository import ScheduledReportRepository
from app.application.scheduledreport.scheduled_reports_dto import ScheduledReportCreateDTO, ScheduledReportUpdateDTO
from app.domain.scheduledreports import ScheduledReport
from app.helpers.jsend_response import jsend_success, jsend_fail

class ScheduledReportService:
    def __init__(self, repo: ScheduledReportRepository):
        self.repo = repo

    def create_report(self, dto:ScheduledReportCreateDTO):
        entity_report = ScheduledReport(**dto.__dict__)

        return jsend_success(self.repo.create_report(entity_report))
    
    def update_report(self, dto:ScheduledReportUpdateDTO):

        entity_report = ScheduledReport(**dto.__dict__)

        return jsend_success(self.repo.update_report(entity_report))
    
    def get_all(self):

        return jsend_success(self.repo.get_all())

    async def execute_due_reports(self):
        due_reports = self.repo.get_due_reports()
        results = []

        for r in due_reports:

            generated_file = self._generate_report(r)

            if r.recipients:
                await self._send_report_by_email(r, generated_file)

            self.repo.update_run_dates(r)
            results.append(r.name)

        return jsend_success({"executed": results})

    def _generate_report(self, report:ScheduledReport):

        view_name = report.name.strip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        reports_dir = os.path.join(os.getcwd(), "app", "shared", "reports")
        os.makedirs(reports_dir, exist_ok=True)

        file_path = os.path.join(reports_dir, f"{view_name}_{timestamp}.xlsx")

        try:

            query = f"SELECT * FROM {view_name};"
            df = pd.read_sql(query, self.repo.db.bind)

            # Guardar Excel
            df.to_excel(file_path, index=False)

            print(f"Reporte generado: {file_path}")
            return file_path

        except Exception as e:
            print(f"Error generando {view_name}: {str(e)}")
            return None

    async def _send_report_by_email(self, report : ScheduledReport, file_path):
        try:

            message = MessageSchema(
                subject=f"Reporte automático: {report.name}",
                recipients=[report.recipients],
                body=f"Hola, adjunto el reporte generado automáticamente: {report.name}",
                subtype=MessageType.html,
                attachments=[file_path]
            )

            fm = FastMail(conf)
            await fm.send_message(message)

            print(f"Correo enviado a {report.recipients} con {file_path}")

        except Exception as e:
            print(f"Error enviando correo: {str(e)}")

    def get_mysql_views(self):

        return jsend_success(self.repo.get_mysql_views())
