from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class EmployeeShift:
    id: int
    employee_id: int
    shift_id: int
    start_date: date
    end_date: Optional[date]