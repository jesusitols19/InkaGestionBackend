from decimal import Decimal
from unittest import result
from io import BytesIO
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from app.domain import employee
from app.infrastructure.payrolls_repository import PayrollRepository
from app.application.payroll.payroll_dto import PayrollCreateDTO
from app.domain.payrolls import Payroll
from app.domain.payrollitems import PayrollItem
from app.infrastructure.employee_repository import EmployeeRepository
from app.infrastructure.payroll_periods_repository import PayrollPeriodRepository
from app.infrastructure.attendance_record_repository import AttendanceRecordRepository
from app.infrastructure.payroll_items_repository import PayrollItemRepository
from app.infrastructure.user_repository import UserRepository
from app.infrastructure.advances_repository import AdvanceRepository
from app.helpers.jsend_response import jsend_success, jsend_fail



class PayrollService:

    def __init__(
            self, 
            repo: PayrollRepository, 
            employee_repo: EmployeeRepository, 
            payroll_periods_repo: PayrollPeriodRepository,
            payroll_item_repo: PayrollItemRepository,
            attendance_record_repo: AttendanceRecordRepository,
            user_repo: UserRepository,
            advance_repo: AdvanceRepository):
        
        self.repo = repo
        self.employee_repo = employee_repo
        self.payroll_periods_repo = payroll_periods_repo
        self.payroll_item_repo = payroll_item_repo
        self.attendance_record_repo = attendance_record_repo
        self.user_repo = user_repo
        self.advance_repo = advance_repo

    # def get_all_payrolls(self):
    #     payrolls = self.repo.get_all()
    #     return jsend_success(payrolls)

    def get_all_payrolls(self):
        payrolls = self.repo.get_all()
        result = []

        for p in payrolls:
            # Obtener datos del empleado
            employee = self.employee_repo.find_by_employee_id(p.employee_id)
            employee_info = {
                "id": employee.id,
                "name": employee.nombre if employee else None
            } if employee else None


            # Obtener usuario que procesó la planilla (si aplica)
            processed_by_info = None
            if p.processed_by:
                processed_user = self.user_repo.find_by_id(p.processed_by)
                processed_by_info = {
                    "id": processed_user.id,
                    "name": processed_user.nombre
                } if processed_user else None

            # Construir respuesta limpia
            payroll_dict = {
                "id": p.id,
                "period": p.period_id,
                "employee": employee_info,
                "gross": p.gross,
                "total_earnings": p.total_earnings,
                "total_deductions": p.total_deductions,
                "net_pay": p.net_pay,
                "processed_by": processed_by_info,
                "processed_at": p.processed_at,
                "created_at": p.created_at
            }

            result.append(payroll_dict)

        return jsend_success(result)

    def generate_payroll(self, dto: PayrollCreateDTO) -> Payroll:

        employee = self.employee_repo.find_by_employee_id(dto.employee_id)
        if not employee:
            return jsend_fail({"employee_id": "Empleado no existe."})
        
        period = self.payroll_periods_repo.find_by_id(dto.period_id)
        if not period:
            return jsend_fail({"period_id": "El periodo de la planilla no existe."})
        
        existing = self.repo.find_by_employee_and_period(dto.employee_id, dto.period_id)
        if existing:
            return jsend_fail({"message": "Ya existe una planilla para este empleado en este periodo."})
        
        earnings = []
        deductions = []

        salary = Decimal(str(employee.salary_base or "0"))

        earnings.append(PayrollItem(
            item_type="EARNING",
            description="Sueldo básico",
            amount=salary
        ))

        afp = (salary * Decimal("0.10")).quantize(Decimal("0.01"))

        deductions.append(PayrollItem(
            item_type="DEDUCTION",
            description="Descuento AFP (10%)",
            amount=afp
        ))

        advances = self.advance_repo.find_by_employee_and_status(dto.employee_id, "PAID")

        sum_advances = Decimal("0.0")

        for adv in advances:
            approved_date = adv.approved_at.date()

            if approved_date >= period.start_date and approved_date <= period.end_date:
                sum_advances += Decimal(str(adv.amount))

        if sum_advances > 0:
            deductions.append(PayrollItem(
                item_type="DEDUCTION",
                description="Adelantos de sueldo",
                amount=sum_advances
            ))

        total_earnings = sum(Decimal(str(e.amount)) for e in earnings)
        total_deductions = sum(Decimal(str(d.amount)) for d in deductions)

        net_pay = total_earnings - total_deductions

        payroll = Payroll(
            period_id=dto.period_id,
            employee_id=dto.employee_id,
            gross=total_earnings,
            total_earnings=total_earnings,
            total_deductions=total_deductions,
            net_pay=net_pay,
            processed_by=dto.processed_by
        )

        payroll_created = self.repo.create_payroll(payroll)

        for item in earnings + deductions:
            item.payroll_id = payroll_created.id
            self.payroll_item_repo.create_payroll_item(item)

        return jsend_success({
            "message": "Planilla generada exitosamente.",
            "payroll_id": payroll_created.id,
            "net_pay": payroll_created.net_pay
        })
    

    def export_payroll_to_excel(self, planillaId: int):
        payroll = self.repo.find_by_id(planillaId)

        if not payroll:
            return jsend_fail({"message": "La planilla no existe."})

        employee = self.employee_repo.find_by_employee_id(payroll.employee_id)
        payroll_items = self.payroll_item_repo.get_by_payroll(planillaId)

        wb = Workbook()
        ws = wb.active
        ws.title = "Planilla"

        # ---- Estilos ----
        bold_font = Font(bold=True)
        title_font = Font(size=16, bold=True)
        subtitle_font = Font(size=13, bold=True)
        center = Alignment(horizontal="center")
        left = Alignment(horizontal="left")

        thin_border = Border(
            left=Side(style="thin"), right=Side(style="thin"),
            top=Side(style="thin"), bottom=Side(style="thin")
        )

        header_fill = PatternFill(start_color="BDD7EE", end_color="BDD7EE", fill_type="solid")
        table_header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
        row_alt_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
        total_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

        # ---- Título ----
        ws.append(["", "Reporte de Planilla"])
        ws["B1"].font = title_font
        ws["B1"].alignment = left

        ws.append(["", "", ""])  # espacio

        # ---- Info del empleado ----
        ws.append(["", "Empleado:", f"{employee.nombre if employee else 'N/A'}"])
        ws["B3"].font = subtitle_font
        ws["C3"].font = Font(size=12)

        ws.append(["", "", ""])  # --> ESTE ES EL ESPACIO QUE PEDISTE
        ws.append(["", "", ""])  # (doble espacio para que se vea mejor)

        # ---- Cabecera de Tabla ----
        ws.append(["", "Descripción", "Tipo", "Monto"])
        header_row = ws.max_row
        for col in ["B", "C", "D"]:
            cell = ws[f"{col}{header_row}"]
            cell.font = bold_font
            cell.alignment = center
            cell.fill = table_header_fill
            cell.border = thin_border

        # ---- Items ----
        alternate = False
        for item in payroll_items:
            ws.append(["", item.description, item.item_type, float(item.amount)])
            row = ws.max_row

            for col in ["B", "C", "D"]:
                cell = ws[f"{col}{row}"]
                cell.border = thin_border
                cell.alignment = left if col != "D" else center

                if alternate:
                    cell.fill = row_alt_fill

            alternate = not alternate

        ws.append([""])  # espacio

        # ---- Totales ----
        totals = [
            ("Total Ganancias:", float(payroll.total_earnings)),
            ("Total Deducciones:", float(payroll.total_deductions)),
            ("Pago Neto:", float(payroll.net_pay)),
        ]

        for label, value in totals:
            ws.append(["", label, "", value])
            row = ws.max_row

            ws[f"B{row}"].font = bold_font
            ws[f"B{row}"].alignment = left
            ws[f"B{row}"].fill = total_fill
            ws[f"D{row}"].font = Font(bold=True)
            ws[f"D{row}"].alignment = center
            ws[f"D{row}"].fill = total_fill

            ws[f"B{row}"].border = thin_border
            ws[f"D{row}"].border = thin_border

        # ---- Ajustar ancho de columnas ----
        for col in ws.columns:
            max_len = 0
            col_letter = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_len = max(max_len, len(str(cell.value)))
            ws.column_dimensions[col_letter].width = max_len + 4

        # ---- Exportar ----
        stream = BytesIO()
        wb.save(stream)
        stream.seek(0)

        filename = f"planilla_{planillaId}.xlsx"

        return StreamingResponse(
            stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    

    def export_payroll_to_pdf(self, planillaId: int):
        payroll = self.repo.find_by_id(planillaId)
        if not payroll:
            return jsend_fail({"message": "La planilla no existe."})

        payroll_items = self.payroll_item_repo.get_by_payroll(planillaId)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # --- Título ---
        elements.append(Paragraph(f"Reporte de Planilla #{planillaId}", styles["Title"]))
        elements.append(Spacer(1, 12))

        # --- Tabla de Items ---
        data = [["Descripción", "Tipo", "Monto (S/.)"]]
        for item in payroll_items:
            data.append([
                item.description,
                "Ingreso" if item.item_type == "EARNING" else "Descuento",
                f"{float(item.amount):.2f}",
            ])

        # Totales
        data.append(["", "", ""])
        data.append(["Total Ingresos", "", f"{float(payroll.total_earnings):.2f}"])
        data.append(["Total Descuentos", "", f"{float(payroll.total_deductions):.2f}"])
        data.append(["Pago Neto", "", f"{float(payroll.net_pay):.2f}"])

        table = Table(data, colWidths=[8 * cm, 4 * cm, 4 * cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ]))

        elements.append(table)

        # --- Generar PDF ---
        doc.build(elements)

        buffer.seek(0)
        filename = f"planilla_{planillaId}.pdf"

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )




        

