from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class Advance:
    id: Optional[int] = None
    employee_id: int = None
    amount: Decimal = None
    requested_by: Optional[int] = None
    requested_at: Optional[datetime] = None
    status: str = None # 'PENDING' | 'APPROVED' | 'REJECTED' | 'PAID'
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    deducted_from_payroll: bool = None
    note: Optional[str] = None
