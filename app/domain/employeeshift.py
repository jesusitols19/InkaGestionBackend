from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class EmployeeShift:
    id: Optional[int] = None
    employee_id: int = None
    shift_id: int = None
    start_date: date = None
    end_date: Optional[date] = None