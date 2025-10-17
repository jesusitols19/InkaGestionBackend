from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    nombre: str
    correo: str
    password: str
    role_id: int = 2

class UserUpdateDTO(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    password: Optional[str] = None
    active: Optional[bool] = None