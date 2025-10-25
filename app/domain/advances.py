from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class Advance:
    id: int
    employee_id: int
    amount: Decimal
    requested_by: Optional[int]
    requested_at: Optional[datetime]
    status: str  # 'PENDING' | 'APPROVED' | 'REJECTED' | 'PAID'
    approved_by: Optional[int]
    approved_at: Optional[datetime]
    deducted_from_payroll: bool
    note: Optional[str]
