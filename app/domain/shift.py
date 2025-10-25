from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

@dataclass
class Shift:
    id: Optional[int] = None
    name: str = None
    start_time: time = None
    end_time: time = None
    tolerance_minutes: int = None
    description: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None