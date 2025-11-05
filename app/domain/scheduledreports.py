from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class ScheduledReport:
    id: Optional[int] = None
    name : str  = None
    frequency : str  = None
    last_run : Optional[datetime] = None
    next_run : Optional[datetime] = None
    recipients : Optional[str] = None
    template : Optional[str] = None
    active : bool = None
    created_by : Optional[int] = None
    created_at : datetime = None