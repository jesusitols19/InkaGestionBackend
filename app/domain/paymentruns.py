from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PaymentRun:
    id: Optional[int] = None
    run_date: Optional[datetime] = None
    total_amount: float = 0.0
    file_name: Optional[str] = None
    status: str = "PENDING"  # 'PENDING', 'PROCESSED', 'FAILED'
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None