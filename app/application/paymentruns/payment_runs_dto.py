from pydantic import BaseModel

class PaymentRunsCreateDTO(BaseModel):
    total_amount: float
    file_name: str
    created_by: int
