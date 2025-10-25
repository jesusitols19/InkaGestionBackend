from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class PayrollItem:
    id: Optional[int] = None
    payroll_id: int = None
    item_type: str = None  # 'EARNING' | 'DEDUCTION'
    code: Optional[str] = None
    description: Optional[str] = None
    amount: Decimal = None
    created_at: Optional[datetime] = None
