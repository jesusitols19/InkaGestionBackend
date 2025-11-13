from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal

@dataclass
class User:
    id: int
    nombre: str
    correo: str
    role_id: int
    password_hash: str
    active: bool
    failed_login_attempts: int
    last_login: datetime | None
    created_at: datetime | None
    updated_at: datetime | None