from pydantic import BaseModel

class PaymentRunItemCreateDTO(BaseModel):
    run_id : int
    employee_id : int
    amount: float
    bank_account: str
