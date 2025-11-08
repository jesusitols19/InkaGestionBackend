from sqlalchemy import Column, BigInteger, Integer, DECIMAL, DateTime, Enum, String, TIMESTAMP, text, ForeignKey
from app.infrastructure.database import Base
from app.domain.paymentruns import PaymentRun
from sqlalchemy.orm import Session
from app.helpers.orm_mapper import to_entity, to_model

class PaymentRunModel(Base):
    __tablename__ = "payment_runs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    run_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    total_amount = Column(DECIMAL(14, 2), nullable=False, server_default=text("0.00"))
    file_name = Column(String(255), nullable=True)
    status = Column(Enum("PENDING", "PROCESSED", "FAILED"), nullable=False, server_default=text("'PENDING'"))
    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class PaymentRunRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(PaymentRunModel).all()

    def create_payment_runs(self, paymentruns : PaymentRun) -> PaymentRun:

        newPaymentRun = to_model(paymentruns, PaymentRunModel)

        self.db.add(newPaymentRun)
        self.db.commit()
        self.db.refresh(newPaymentRun)

        return to_entity(newPaymentRun, PaymentRun)
    
    def find_by_id(self, paymentRunId : int) -> PaymentRun:

        paymentRun = self.db.query(PaymentRunModel).filter(PaymentRunModel.id == paymentRunId).first()

        return to_entity(paymentRun, PaymentRun)
    

    def update(self, paymentrun : PaymentRun):

        updatePaymentRun = to_model(paymentrun, PaymentRunModel)

        self.db.commit()
        self.db.refresh(updatePaymentRun)

        return to_entity(updatePaymentRun, PaymentRun)