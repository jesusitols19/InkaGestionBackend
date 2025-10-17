from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.dependencies import get_attendance_record_service
from app.application.attendancerecord.attendance_record_dto import AttendanceStartDTO
from app.application.attendancerecord.attendance_record_dto import AttendanceEndDTO
from app.infrastructure.attendance_record_repository import AttendanceRecordRepository
from app.infrastructure.employee_shift_repository import EmployeeShiftRepository
from app.infrastructure.shift_repository import ShiftRepository
from app.infrastructure.employee_repository import EmployeeRepository
from app.application.attendancerecord.attendance_record_service import AttendanceRecordService

router = APIRouter()


@router.get("/inicio-modulo-asistencia/{employee_id}")
def get_attendance(employee_id: int, db: Session = Depends(get_db)):
    service = get_attendance_record_service(db)
    return service.get_attendance(employee_id)


@router.get("/obtener-turno-activo/{employee_id}")
def get_active_shift(employee_id: int, db: Session = Depends(get_db)):
    service = get_attendance_record_service(db)
    return service.get_active_shift(employee_id)

@router.post("/crear-asistencia")
def start_attendance(dto: AttendanceStartDTO, db: Session = Depends(get_db)):
    service = get_attendance_record_service(db)
    return service.start_attendance(dto)

@router.post("/finalizar-asistencia")
def end_attendance(dto: AttendanceEndDTO, db: Session = Depends(get_db)):
    service = get_attendance_record_service(db)
    return service.end_attendance(dto)




