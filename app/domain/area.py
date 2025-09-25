from dataclasses import dataclass
from datetime import datetime

@dataclass
class Area:
    id: int
    name: str
    code: str | None
    description: str | None
    active:bool
    created_at: datetime