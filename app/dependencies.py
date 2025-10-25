from app.infrastructure.database import get_db
from app.infrastructure.employee_repository import EmployeeRepository
from app.infrastructure.area_repository import AreaRepository
from app.infrastructure.attendance_record_repository import AttendanceRecordRepository
from app.infrastructure.employee_shift_repository import EmployeeShiftRepository
from app.infrastructure.shift_repository import ShiftRepository
from app.infrastructure.payroll_periods_repository import PayrollPeriodRepository
from app.infrastructure.payrolls_repository import PayrollRepository
from app.infrastructure.payroll_items_repository import PayrollItemRepository
from app.infrastructure.user_repository import UserRepository
from app.application.payrollperiods.payroll_periods_service import PayrollPeriodService
from app.application.payroll.payroll_service import PayrollService
from app.application.employee.employee_service import EmployeeService
from app.application.attendancerecord.attendance_record_service import AttendanceRecordService

def get_employee_service(db):
    employee_repo = EmployeeRepository(db)
    area_repo = AreaRepository(db)
    return EmployeeService(employee_repo, area_repo)


def get_attendance_record_service(db):
    attendance_record_repo = AttendanceRecordRepository(db)
    employee_repo = EmployeeRepository(db)
    employee_shift_repo = EmployeeShiftRepository(db)
    shift_repo = ShiftRepository(db)
    return AttendanceRecordService(attendance_record_repo, employee_repo, employee_shift_repo, shift_repo)


def get_payroll_period_service(db):
    payroll_period_repo = PayrollPeriodRepository(db)
    return PayrollPeriodService(payroll_period_repo)


def get_payroll_service(db):

    payroll_repo = PayrollRepository(db)
    employee_repo = EmployeeRepository(db)
    payroll_periods_repo = PayrollPeriodRepository(db)
    payroll_item_repo = PayrollItemRepository(db)
    attendance_record_repo = AttendanceRecordRepository(db)
    user_repo = UserRepository(db)
    return PayrollService(payroll_repo, employee_repo, payroll_periods_repo, payroll_item_repo, attendance_record_repo, user_repo)