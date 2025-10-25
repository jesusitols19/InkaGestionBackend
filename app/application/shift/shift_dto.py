from pydantic import BaseModel

class ShiftCreateDTO(BaseModel):
    name: str
    start_time: str
    end_time: str
    tolerance_minutes: int
    description: str
    created_by: int