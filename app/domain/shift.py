from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

@dataclass
class Shift:
    id: int
    name: str
    start_time: time
    end_time: time
    tolerance_minutes: int
    description: Optional[str]
    created_by: Optional[int]
    created_at: Optional[datetime]