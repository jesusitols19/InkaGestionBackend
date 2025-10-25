from sqlalchemy.orm import Session
from sqlalchemy import Column, BigInteger, Integer, DECIMAL, ForeignKey, DateTime, TIMESTAMP, text
from app.infrastructure.database import Base
from app.domain.payrolls import Payroll
from app.helpers.orm_mapper import to_entity, to_model


class PayrollModel(Base):
    __tablename__ = "payrolls"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    period_id = Column(Integer, nullable=False)
    employee_id = Column(Integer, nullable=False)
    gross = Column(DECIMAL(12, 2), nullable=False, server_default=text("0.00"))
    total_earnings = Column(DECIMAL(12, 2), nullable=False, server_default=text("0.00"))
    total_deductions = Column(DECIMAL(12, 2), nullable=False, server_default=text("0.00"))
    net_pay = Column(DECIMAL(12, 2), nullable=False, server_default=text("0.00"))
    processed_by = Column(Integer, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class PayrollRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        records = self.db.query(PayrollModel).all()
        return [to_entity(record, Payroll) for record in records]

    def find_by_id(self, payroll_id: int):
        return self.db.query(PayrollModel).filter(PayrollModel.id == payroll_id).first()

    def find_by_period(self, period_id: int):
        return self.db.query(PayrollModel).filter(PayrollModel.period_id == period_id).all()

    def find_by_employee(self, employee_id: int):
        return self.db.query(PayrollModel).filter(PayrollModel.employee_id == employee_id).all()
    
    def find_by_employee_and_period(self, employee_id: int, period_id: int):
        return self.db.query(PayrollModel).filter(
            PayrollModel.employee_id == employee_id,
            PayrollModel.period_id == period_id
        ).first()
    

    def create_payroll(self, payroll: Payroll) -> Payroll:

        new_payroll = to_model(payroll, PayrollModel)

        self.db.add(new_payroll)
        self.db.commit()
        self.db.refresh(new_payroll)

        return to_entity(new_payroll, Payroll)


