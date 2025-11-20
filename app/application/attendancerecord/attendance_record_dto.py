# app/application/attendance/attendance_dto.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AttendanceStartDTO(BaseModel):
    employee_id: int
    supervisor_user_id: int
    timestamp: Optional[datetime] = None
    justification: Optional[str] = None
    lat: Optional[float]
    lng: Optional[float]

class AttendanceEndDTO(BaseModel):
    employee_id: int
    supervisor_user_id: int
    timestamp: Optional[datetime] = None
    lat: Optional[float]
    lng: Optional[float]

# DTO para filtros si los quisieras
class AttendanceFilterDTO(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    limit: Optional[int] = 30
