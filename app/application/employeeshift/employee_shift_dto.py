from pydantic import BaseModel

class EmployeeShiftCreateDTO(BaseModel):
    employee_id: int
    shift_id: int
    start_date: str
    end_date: str
