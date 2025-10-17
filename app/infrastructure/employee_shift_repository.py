from sqlalchemy.orm import Session
from sqlalchemy import Column, Date, SmallInteger, Integer, String, Time, TIMESTAMP, or_, text
from datetime import datetime, date, timedelta, time
from app.infrastructure.database import Base

class EmployeeShiftModel(Base):
    __tablename__ = "employee_shifts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, nullable=False)
    shift_id = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)


# Repositorio
class EmployeeShiftRepository:
    def __init__(self, db: Session):
        self.db = db

    # Devuelve el turno activo para el empleado en la fecha indicada (o None)
    def get_active_employee_shift(self, employee_id: int, on_date: date):
        employeeShift = self.db.query(EmployeeShiftModel).filter(
            EmployeeShiftModel.employee_id == employee_id,
            EmployeeShiftModel.start_date <= on_date,
            or_(EmployeeShiftModel.end_date == None, EmployeeShiftModel.end_date >= on_date)
        ).first()
        if not employeeShift:
            return None
        return employeeShift
