from pydantic import BaseModel
from datetime import date
from typing import Optional

class EmployeeFilterDTO(BaseModel):
    nombre: Optional[str] = None
    documento: Optional[str] = None
    telefono: Optional[str] = None
    area_id: Optional[int] = None
    salario_min: Optional[float] = None
    salario_max: Optional[float] = None
    solo_activos: Optional[bool] = None

class EmployeeCreateDTO(BaseModel):
    employee_number: Optional[str] = None
    nombre: str
    documento: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    area_id: Optional[int] = None
    hire_date: Optional[date] = None
    salary_base: float
    contract_type: Optional[str] = None
    bank_account: Optional[str] = None
    active: bool = True



class EmployeeUpdateDTO(BaseModel):
    employee_number: Optional[str] = None
    nombre: Optional[str] = None
    documento: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    area_id: Optional[int] = None
    hire_date: Optional[date] = None
    salary_base: Optional[float] = None
    contract_type: Optional[str] = None
    bank_account: Optional[str] = None
    active: Optional[bool] = None
