from pydantic import BaseModel
from datetime import date, datetime

class ScheduledReportCreateDTO(BaseModel):
    name: str
    frequency: str
    next_run: datetime
    recipients: str
    template: str
    created_by: int

class ScheduledReportUpdateDTO(BaseModel):
    id: int
    name: str
    frequency: str
    next_run: datetime
    last_run: datetime
    recipients: str
    template: str
    active: bool
    created_by: int