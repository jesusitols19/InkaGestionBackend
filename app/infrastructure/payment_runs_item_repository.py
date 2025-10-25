from sqlalchemy import Column, BigInteger, Integer, DECIMAL, DateTime, Enum, String, ForeignKey, text
from app.infrastructure.database import Base
from sqlalchemy.orm import Session
from app.domain.paymentrunitems import PaymentRunItem
from app.helpers.orm_mapper import to_entity, to_model

class PaymentRunItemModel(Base):
    __tablename__ = "payment_run_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    run_id = Column(BigInteger, nullable=False)
    employee_id = Column(Integer, nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False)
    bank_account = Column(String(120), nullable=True)
    status = Column(Enum("PENDING", "SENT", "PAID", "REJECTED"), nullable=False, server_default=text("'PENDING'"))
    processed_at = Column(DateTime, nullable=True)


class PaymentRunItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_payment_run_item(self, paymentRunItem : PaymentRunItem) -> PaymentRunItem:

        newPaymentRunItem = to_model(paymentRunItem, PaymentRunItemModel)

        self.db.add(newPaymentRunItem)

        self.db.commit()

        self.db.refresh(newPaymentRunItem)

        return to_entity(newPaymentRunItem,PaymentRunItem)
    

    def find_by_id(self, paymentRunId: int):
        paymentRunItems = self.db.query(PaymentRunItemModel).filter(PaymentRunItemModel.run_id == paymentRunId).all()

        return [to_entity(paymentRunItem, PaymentRunItem) for paymentRunItem in paymentRunItems]