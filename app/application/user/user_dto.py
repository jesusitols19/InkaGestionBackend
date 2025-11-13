from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    nombre: str
    correo: str
    password: str = Field(..., min_length=8)
    role_id: int = 2

class UserUpdateDTO(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=8)
    active: Optional[bool] = None