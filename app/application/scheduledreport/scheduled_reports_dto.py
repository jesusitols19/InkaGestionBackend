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
    start_date: str
    end_date: str
    status: str