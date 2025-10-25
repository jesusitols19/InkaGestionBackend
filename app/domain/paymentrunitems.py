from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PaymentRunItem:
    id: Optional[int] = None
    run_id: int = None
    employee_id: int = None
    amount: float = 0.0
    bank_account: Optional[str] = None
    status: str = "PENDING"  # 'PENDING', 'SENT', 'PAID', 'REJECTED'
    processed_at: Optional[datetime] = None