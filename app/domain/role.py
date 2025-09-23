from dataclasses import dataclass
from datetime import datetime

@dataclass
class Role:
    id: int
    name: str
    description: str | None
    created_at: datetime
