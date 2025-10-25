from pydantic import BaseModel

class PayrollPeriodCreateDTO(BaseModel):
    start_date: str
    end_date: str

class PayrollPeriodUpdateDTO(BaseModel):
    id: int
    start_date: str
    end_date: str
    status: str