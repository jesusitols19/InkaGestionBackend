from pydantic import BaseModel

class AdvanceRequestDTO(BaseModel):
    employee_id: int
    amount: float
    requested_by: int
    note: str

class AdvanceApproveDTO(BaseModel):
    advance_id: int
    approved_by: float
    approve: bool