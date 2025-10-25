from pydantic import BaseModel

class PayrollCreateDTO(BaseModel):
    period_id: int
    employee_id: int
    processed_by: int