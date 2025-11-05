from pydantic import BaseModel

class SystemActivityCreateDTO(BaseModel):
    title: str
    description: str
    icono: str
    created_by: int