from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class PayrollPeriod:
    id: Optional[int] = None
    start_date: date = None
    end_date: date = None
    status: str  = None # 'OPEN' | 'CLOSED'
    created_at: Optional[datetime] = None
