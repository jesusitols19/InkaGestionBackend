from unittest import result
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

        salary = float(employee.salary_base or 0)

        earnings.append(PayrollItem(
            item_type="EARNING",
            description="Sueldo básico",
            amount=salary
        ))

        afp = round(salary * 0.10, 2)
        deductions.append(PayrollItem(
            item_type="DEDUCTION",
            description="Descuento AFP (10%)",
            amount=afp
        ))

        # advances = self.advance_repo.find_by_employee_and_status(dto.employee_id, "PAID")

        # sum_advances = 0.0
        # for adv in advances:
        #     if adv.approved_at >= period.start_date and adv.approved_at <= period.end_date:
        #         sum_advances += adv.amount

        # if sum_advances > 0:
        #     deductions.append(PayrollItem(
        #         item_type="DEDUCTION",
        #         description="Adelantos de sueldo",
        #         amount=sum_advances
        #     ))

        # tardanzas = self.attendance_record_repo.count_tardiness_by_employee_and_period(dto.employee_id, dto.period_id) or 0
        # tardanza_deduction = tardanzas * 10
        # if tardanza_deduction > 0:
        #     deductions.append(PayrollItem(
        #         item_type="DEDUCTION",
        #         description=f"Tardanzas ({tardanzas} días)",
        #         amount=tardanza_deduction
        #     ))


        total_earnings = sum(e.amount for e in earnings)
        total_deductions = sum(d.amount for d in deductions)

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
