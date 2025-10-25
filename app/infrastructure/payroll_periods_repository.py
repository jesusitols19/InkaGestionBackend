from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, Date, Enum, TIMESTAMP, text
from app.infrastructure.database import Base
from app.domain.payrollperiods import PayrollPeriod
from app.helpers.orm_mapper import to_entity, to_model

class PayrollPeriodModel(Base):
    __tablename__ = "payroll_periods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum("OPEN", "CLOSED"), nullable=False, server_default=text("'OPEN'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class PayrollPeriodRepository:
    def __init__(self, db: Session):
        self.db = db
        self.query = db.query(PayrollPeriodModel)

    def get_all(self):
        return self.query.all()

    def find_by_id(self, period_id: int):
        return self.query.filter(PayrollPeriodModel.id == period_id).first()

    def find_open_period(self):
        return self.query.filter(PayrollPeriodModel.status == "OPEN").first()
    
    def find_closed_periods(self):
        return self.query.filter(PayrollPeriodModel.status == "CLOSED").all()
    
    def create_payroll_period(self, payroll_period: PayrollPeriod) -> PayrollPeriod:

        new_period = to_model(payroll_period, PayrollPeriodModel)

        self.db.add(new_period)
        self.db.commit()
        self.db.refresh(new_period)
        
        return to_entity(new_period, PayrollPeriod)
    

    def update_payroll_period(self, payroll_period: PayrollPeriod) -> PayrollPeriod:
        
        existing_period = self.query.filter(PayrollPeriodModel.id == payroll_period.id).first()
        if not existing_period:
            return None

        for key, value in payroll_period.__dict__.items():
            setattr(existing_period, key, value)

        self.db.commit()
        self.db.refresh(existing_period)

        return to_entity(existing_period, PayrollPeriod)



