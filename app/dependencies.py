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
from app.infrastructure.payment_runs_repository import PaymentRunRepository
from app.infrastructure.payment_runs_item_repository import PaymentRunItemRepository
from app.infrastructure.advances_repository import AdvanceRepository
from app.infrastructure.views.dashboard.v_bi_analytics_repository import VBiAnalyticsRepository
from app.infrastructure.views.dashboard.v_costos_personal_mensual_repository import VCostosPersonalMensualRepository
from app.infrastructure.views.dashboard.v_eficiencia_general_hoy_repository import VEficienciaGeneralHoyRepository
from app.infrastructure.views.dashboard.v_gasto_personal_total_repository import VGastoPersonalTotalRepository
from app.infrastructure.views.dashboard.v_horas_trabajadas_total_general_repository import VHorasTrabajadasTotalGeneralRepository
from app.infrastructure.views.dashboard.v_promedio_horas_hoy_repository import VPromedioHorasHoyRepository
from app.infrastructure.views.dashboard.v_total_empleados_repository import VTotalEmpleadosRepository
from app.infrastructure.views.dashboard.v_pagos_pendientes_repository import VPagosPendientesRepository
from app.infrastructure.views.dashboard.v_resumen_asistencia_hoy_repository import VResumenAsistenciaHoyRepository
from app.infrastructure.system_activity_repository import SystemActivityRepository
from app.infrastructure.scheduled_reports_repository import ScheduledReportRepository
from app.infrastructure.advances_repository import AdvanceRepository
from app.application.payrollperiods.payroll_periods_service import PayrollPeriodService
from app.application.payroll.payroll_service import PayrollService
from app.application.employee.employee_service import EmployeeService
from app.application.attendancerecord.attendance_record_service import AttendanceRecordService
from app.application.shift.shift_service import ShiftService
from app.application.employeeshift.employee_shift_service import EmployeeShiftService
from app.application.paymentruns.payment_runs_service import PaymentRunService
from app.application.advance.advance_service import AdvanceService
from app.application.dashboard.dashboard_service import DashboardService
from app.application.systemactivity.system_activity_service import SystemActivityService
from app.application.scheduledreport.scheduled_reports_service import ScheduledReportService 
from app.application.area.area_service import AreaService

def get_employee_service(db):
    employee_repo = EmployeeRepository(db)
    area_repo = AreaRepository(db)
    return EmployeeService(employee_repo, area_repo)

def get_area_service(db):
    area_repo = AreaRepository(db)
    return AreaService(area_repo)

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
    advance_repo = AdvanceRepository(db)
    return PayrollService(payroll_repo, employee_repo, payroll_periods_repo, payroll_item_repo, attendance_record_repo, user_repo, advance_repo)


def get_shift_service(db):
    shift_repo = ShiftRepository(db)
    return ShiftService(shift_repo)


def get_employee_shift_service(db):
    employee_shift_repo = EmployeeShiftRepository(db)

    return EmployeeShiftService(employee_shift_repo)


def get_payment_run_service(db):

    payment_run_repo = PaymentRunRepository(db)

    payment_run_item_repo = PaymentRunItemRepository(db)

    return PaymentRunService(payment_run_repo, payment_run_item_repo)

def get_advance_service(db):

    advance_repo = AdvanceRepository(db)

    return AdvanceService(advance_repo)

def get_dashboard_service(db):
    
    # Repositorios existentes (KPIs)
    costosPersonalMensualRepository = VCostosPersonalMensualRepository(db)
    eficienciaGeneralHoyRepository = VEficienciaGeneralHoyRepository(db)
    gastoPersonalTotalRepository = VGastoPersonalTotalRepository(db)
    horasTrabajadasTotalGeneralRepository = VHorasTrabajadasTotalGeneralRepository(db)
    promedioHorasHoyRepository = VPromedioHorasHoyRepository(db)
    totalEmpleadosRepository = VTotalEmpleadosRepository(db)
    pagosPendientesRepository = VPagosPendientesRepository(db)
    resumenAsistenciaHoyRepository = VResumenAsistenciaHoyRepository(db)

    # Nuevo Repositorio (BI Charts)
    biAnalyticsRepository = VBiAnalyticsRepository(db) # <--- INSTANCIA NUEVA

    return DashboardService(
        costosPersonalMensualRepository, 
        eficienciaGeneralHoyRepository, 
        gastoPersonalTotalRepository, 
        horasTrabajadasTotalGeneralRepository, 
        promedioHorasHoyRepository, 
        totalEmpleadosRepository,
        pagosPendientesRepository,
        resumenAsistenciaHoyRepository,
        biAnalyticsRepository # <--- PASAR AL SERVICIO
    )

def get_system_activity_service(db):
    systemActivityRepository = SystemActivityRepository(db)

    return SystemActivityService(
        systemActivityRepository
    )


def get_scheduled_report_service(db):

    scheduledReportRepository = ScheduledReportRepository(db)

    return ScheduledReportService(
        scheduledReportRepository
    )
