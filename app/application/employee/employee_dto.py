from pydantic import BaseModel
from typing import Optional

class EmployeeFilterDTO(BaseModel):
    nombre: Optional[str] = None
    documento: Optional[str] = None
    telefono: Optional[str] = None
    area_id: Optional[int] = None
    salario_min: Optional[float] = None
    salario_max: Optional[float] = None
    solo_activos: Optional[bool] = None