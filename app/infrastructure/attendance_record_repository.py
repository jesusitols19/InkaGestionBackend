from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import Column, Date, BigInteger, DECIMAL, Integer,Boolean, String, DateTime, TIMESTAMP, text, Text, Enum
from app.infrastructure.database import Base

from app.domain.attendancerecord import AttendanceRecord
from datetime import datetime, date, timedelta, time
from typing import Optional


class AttendanceRecordModel(Base):
    __tablename__ = "attendance_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, nullable=False)
    supervisor_user_id = Column(Integer, nullable=True)

    record_date = Column(Date, nullable=False)
    time_in = Column(DateTime, nullable=True)
    time_out = Column(DateTime, nullable=True)
    work_hours = Column(DECIMAL(5, 2), nullable=True)
    overtime_hours = Column(DECIMAL(5, 2), nullable=True)
    status = Column(
        Enum("A_TIEMPO", "TARDANZA", "AUSENCIA", "PARCIAL", name="attendance_status_enum"),
        nullable=False,
        server_default=text("'A_TIEMPO'")
    )

    lat_in = Column(DECIMAL(10, 7), nullable=True)
    lng_in = Column(DECIMAL(10, 7), nullable=True)
    lat_out = Column(DECIMAL(10, 7), nullable=True)
    lng_out = Column(DECIMAL(10, 7), nullable=True)

    location_valid_in = Column(Boolean, nullable=False, server_default=text("0"))
    location_valid_out = Column(Boolean, nullable=False, server_default=text("0"))
    device_info = Column(String(255), nullable=True)
    justification = Column(Text, nullable=True)

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)


# Repositorio
class AttendanceRecordRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[AttendanceRecord]:
        results = self.db.query(AttendanceRecordModel).all()
        return [self._map_to_entity(row) for row in results]
    
    def find_by_attendance_record_id(self, attendance_record_id: int) -> AttendanceRecord:
        attendance_record = self.db.query(AttendanceRecordModel).filter(AttendanceRecordModel.id == attendance_record_id).first()
        return self._map_to_entity(attendance_record)
    
    # Devuelve asistencia activa (sin time_out) para hoy
    def get_active_attendance(self, employee_id: int, on_date: date):

        active = (
            self.db.query(AttendanceRecordModel)
            .filter(
                AttendanceRecordModel.employee_id == employee_id,
                AttendanceRecordModel.record_date == on_date,
                AttendanceRecordModel.time_out == None
            )
            .first()
        )

        if not active:
            yesterday = on_date - timedelta(days=1)
            active = (
                self.db.query(AttendanceRecordModel)
                .filter(
                    AttendanceRecordModel.employee_id == employee_id,
                    AttendanceRecordModel.record_date == yesterday,
                    AttendanceRecordModel.time_out == None
                )
                .first()
            )

        return active
    
    # Saber si existe registro para hoy (cualquiera)
    def exists_record_today(self, employee_id: int, on_date: date) -> bool:
        r = self.db.query(AttendanceRecordModel).filter(
            AttendanceRecordModel.employee_id == employee_id,
            AttendanceRecordModel.record_date == on_date
        ).first()
        return True if r else False
    
    # Listado histórico (últimos N)
    def list_history(self, employee_id: int, limit: int = 50):
        rows = self.db.query(AttendanceRecordModel).filter(
            AttendanceRecordModel.employee_id == employee_id
        ).order_by(AttendanceRecordModel.record_date.desc(), AttendanceRecordModel.time_in.desc()).limit(limit).all()
        return rows
    
    # def get_count_tardiness_by_employee(self, employee_id: int, period_id: int) -> int:
    #     return self.db.query(AttendanceRecordModel).filter(
    #         AttendanceRecordModel.employee_id == employee_id,
    #         AttendanceRecordModel.record_date.between(period_id.start_date, period_id.end_date),
    #         AttendanceRecordModel.status == "TARDANZA"
    #     ).count()
    

    # Crear registro de inicio
    def create_start(self, employee_id: int, supervisor_user_id: int, 
                     timestamp: datetime, status: str, justification: Optional[str] = None,
                     lat: Optional[float] = None, lng: Optional[float] = None, location_valid: bool = False):
        rec = AttendanceRecordModel(
            employee_id=employee_id,
            supervisor_user_id=supervisor_user_id,
            record_date=timestamp.date(),
            time_in=timestamp,
            status=status,
            justification=justification,
            lat_in=lat,
            lng_in=lng,
            location_valid_in=location_valid,
        )
        self.db.add(rec)
        self.db.commit()
        self.db.refresh(rec)
        return rec
    
    # Finalizar registro activo
    def end_attendance(self, attendance_record: AttendanceRecordModel, timestamp: datetime, 
                       work_hours: Decimal, overtime_hours: Decimal,
                       lat: Optional[float] = None, lng: Optional[float] = None,
                       location_valid: bool = False):
        attendance_record.time_out = timestamp
        attendance_record.work_hours = work_hours
        attendance_record.overtime_hours = overtime_hours
        attendance_record.lat_out = lat
        attendance_record.lng_out = lng
        attendance_record.location_valid_out = location_valid
        self.db.commit()
        self.db.refresh(attendance_record)
        return attendance_record

    def _map_to_entity(self, row: AttendanceRecordModel) -> AttendanceRecord:
        return AttendanceRecord(
            id=row.id,
            employee_id=row.employee_id,
            supervisor_user_id=row.supervisor_user_id,
            record_date=row.record_date,
            time_in=row.time_in,
            time_out=row.time_out,
            work_hours=row.work_hours,
            overtime_hours=row.overtime_hours,
            status=row.status,
            lat_in=row.lat_in,
            lng_in=row.lng_in,
            lat_out=row.lat_out,
            lng_out=row.lng_out,
            location_valid_in=row.location_valid_in,
            location_valid_out=row.location_valid_out,
            device_info=row.device_info,
            justification=row.justification,
            created_at=row.created_at,
            updated_at=row.updated_at
        )