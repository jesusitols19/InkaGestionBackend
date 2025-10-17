from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

@dataclass
class AttendanceRecord:
    id: int
    employee_id: int
    supervisor_user_id: Optional[int]
    record_date: date
    time_in: Optional[datetime]
    time_out: Optional[datetime]
    work_hours: Optional[Decimal]
    overtime_hours: Optional[Decimal]
    status: str  # 'A_TIEMPO', 'TARDANZA', 'AUSENCIA', 'PARCIAL'
    lat_in: Optional[Decimal]
    lng_in: Optional[Decimal]
    lat_out: Optional[Decimal]
    lng_out: Optional[Decimal]
    location_valid_in: bool
    location_valid_out: bool
    device_info: Optional[str]
    justification: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]