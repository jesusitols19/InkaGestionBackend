from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class Payroll:
    id: Optional[int] = None
    period_id: int = None
    employee_id: int = None
    gross: Decimal = None
    total_earnings: Decimal = None
    total_deductions: Decimal = None
    net_pay: Decimal = None
    processed_by: Optional[int] = None
    processed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
