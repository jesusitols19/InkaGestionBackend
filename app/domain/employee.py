from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal

@dataclass
class Employee:
    id: int
    employee_number: str | None
    nombre: str
    documento: str | None
    correo: str | None
    telefono: str | None
    area_id: int | None
    hire_date: date | None
    salary_base: Decimal
    contract_type: str | None
    bank_account: str | None
    active: bool
    created_at: datetime
    updated_at: datetime | None