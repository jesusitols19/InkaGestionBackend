from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class SystemActivity:
    id: Optional[int] = None
    title: str = None
    description: str = None
    icono: str = None
    created_by: int = None
    created_at: Optional[datetime] = None