from app.infrastructure.attendance_record_repository import AttendanceRecordRepository
from app.infrastructure.employee_repository import EmployeeRepository
from app.infrastructure.employee_shift_repository import EmployeeShiftRepository
from app.infrastructure.shift_repository import ShiftRepository
from app.domain.attendancerecord import AttendanceRecord
from app.helpers.jsend_response import jsend_success
from app.helpers.jsend_response import jsend_fail
from datetime import datetime, date, timedelta, time
from decimal import Decimal, ROUND_HALF_UP
from typing import List
from app.application.attendancerecord.attendance_record_dto import AttendanceStartDTO
from app.application.attendancerecord.attendance_record_dto import AttendanceEndDTO


class AttendanceRecordService:
    def __init__(self, repo: AttendanceRecordRepository, employee_repo: EmployeeRepository, employee_shift_repo: EmployeeShiftRepository, shift_repo: ShiftRepository):
        self.repo = repo
        self.employee_repo = employee_repo
        self.employee_shift_repo = employee_shift_repo
        self.shift_repo = shift_repo


    def get_attendance(self, employee_id: int, limit: int = 50):

        empleado = self.employee_repo.find_by_employee_id(employee_id)

        if not empleado:
            return jsend_fail({"message": "Empleado no encontrado"})
        
        today = date.today()

        active = self.repo.get_active_attendance(employee_id, today)

        history = self.repo.list_history(employee_id, limit)

        def map_rec(r):
            return {
                "id": r.id,
                "record_date": r.record_date,
                "time_in": r.time_in,
                "time_out": r.time_out,
                "work_hours": float(r.work_hours) if r.work_hours is not None else None,
                "overtime_hours": float(r.overtime_hours) if r.overtime_hours is not None else None,
                "status": r.status,
                "justification": r.justification
            }
        
        return jsend_success({
            "active_record": map_rec(active) if active else None,
            "records": [map_rec(r) for r in history]
        })
    
    def get_active_shift(self, employee_id: int):

        today = date.today()

        employee_shift = self.employee_shift_repo.get_active_employee_shift(employee_id, today)

        if not employee_shift:
            return jsend_fail({"message": "Empleado no tiene turno asignado hoy"})

        shift = self.shift_repo.get_shift_by_id(employee_shift.shift_id)

        if not shift:
            return jsend_fail({"message": "Empleado no tiene turno asignado hoy"})
        
        return jsend_success({
            "shift_name": shift.name,
            "start_time": shift.start_time,
            "end_time": shift.end_time,
            "tolerance_minutes": shift.tolerance_minutes,
            "start_date": employee_shift.start_date,
            "end_date": employee_shift.end_date
        })
    

    def start_attendance(self, dto: AttendanceStartDTO):

        empleado = self.employee_repo.find_by_employee_id(dto.employee_id)

        if not empleado:
            return jsend_fail({"message": "Empleado no encontrado"})
        
        today = date.today()

        employee_shift = self.employee_shift_repo.get_active_employee_shift(dto.employee_id, today)

        if not employee_shift:
            return jsend_fail({"message": "Empleado no tiene turno asignado hoy"})
        
        shift = self.shift_repo.get_shift_by_id(employee_shift.shift_id)

        if not shift:
            return jsend_fail({"message": "Empleado no tiene turno asignado hoy"})
        
        active = self.repo.get_active_attendance(dto.employee_id, today)
        if active:
            return jsend_fail({"message": "Ya existe una asistencia activa para este empleado hoy"})
        
        
        exists_today = self.repo.exists_record_today(dto.employee_id, today)
        if exists_today:
            return jsend_fail({"message": "Ya existe un registro para este empleado en la fecha de hoy"})
        
        timestamp = dto.timestamp or datetime.now()

        shift_start_dt = datetime.combine(timestamp.date(), shift.start_time)

        allowed_early_dt = shift_start_dt - timedelta(minutes=10)

        if timestamp < allowed_early_dt:
            return jsend_fail({
                "message": "Solo puedes registrar asistencia hasta 10 minutos antes del inicio de tu turno."
            })

        allowed_dt = shift_start_dt + timedelta(minutes=shift.tolerance_minutes or 0)
        status = "A_TIEMPO" if timestamp <= allowed_dt else "TARDANZA"

        
        rec = self.repo.create_start(dto.employee_id, dto.supervisor_user_id, timestamp, status, dto.justification)

        return jsend_success({
            "message": "Asistencia iniciada",
            "attendance": {
                "id": rec.id,
                "time_in": rec.time_in,
                "status": rec.status
            }
        })
    

    def end_attendance(self, dto: AttendanceEndDTO):

        empleado = self.employee_repo.find_by_employee_id(dto.employee_id)

        if not empleado:
            return jsend_fail({"message": "Empleado no encontrado"})
        
        today = date.today()

        active = self.repo.get_active_attendance(dto.employee_id, today)

        if not active:
            return jsend_fail({"message": "No hay asistencia activa para finalizar"})
        
        # timestamp = dto.timestamp or datetime.utcnow()
        timestamp = dto.timestamp or datetime.now()

        delta = timestamp - active.time_in
        hours = delta.total_seconds() / 3600.0
        work_hours = float(Decimal(hours).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

        overtime = max(0.0, work_hours - 8.0)
        overtime_hours = float(Decimal(overtime).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

        rec = self.repo.end_attendance(active, timestamp, work_hours, overtime_hours)

        return jsend_success({
            "message": "Asistencia finalizada",
            "attendance": {
                "id": rec.id,
                "time_out": rec.time_out,
                "work_hours": rec.work_hours,
                "overtime_hours": rec.overtime_hours
            }
        })
        

