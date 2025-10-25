from sqlalchemy.orm import Session
from sqlalchemy import Column, BigInteger, Integer, DECIMAL, Text, Enum, DateTime, Boolean, ForeignKey, text
from app.infrastructure.database import Base


class AdvanceModel(Base):
    __tablename__ = "advances"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False)
    requested_by = Column(Integer, nullable=True)
    requested_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(Enum("PENDING", "APPROVED", "REJECTED", "PAID"), nullable=False, server_default=text("'PENDING'"))
    approved_by = Column(Integer, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    deducted_from_payroll = Column(Boolean, nullable=False, server_default=text("0"))
    note = Column(Text, nullable=True)


class AdvanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(AdvanceModel).all()

    def find_by_id(self, advance_id: int):
        return self.db.query(AdvanceModel).filter(AdvanceModel.id == advance_id).first()

    def find_by_employee(self, employee_id: int):
        return self.db.query(AdvanceModel).filter(AdvanceModel.employee_id == employee_id).all()

    def find_pending(self):
        return self.db.query(AdvanceModel).filter(AdvanceModel.status == "PENDING").all()
