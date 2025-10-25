from sqlalchemy.orm import Session
from sqlalchemy import Column, BigInteger, String, Enum, DECIMAL, TIMESTAMP, ForeignKey, text
from app.infrastructure.database import Base
from app.domain.payrollitems import PayrollItem
from app.helpers.orm_mapper import to_entity, to_model


class PayrollItemModel(Base):
    __tablename__ = "payroll_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    payroll_id = Column(BigInteger, ForeignKey("payrolls.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    item_type = Column(Enum("EARNING", "DEDUCTION"), nullable=False)
    code = Column(String(50), nullable=True)
    description = Column(String(255), nullable=True)
    amount = Column(DECIMAL(12, 2), nullable=False, server_default=text("0.00"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class PayrollItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(PayrollItemModel).all()

    def get_by_payroll(self, payroll_id: int):
        return self.db.query(PayrollItemModel).filter(PayrollItemModel.payroll_id == payroll_id).all()

    def find_by_id(self, item_id: int):
        return self.db.query(PayrollItemModel).filter(PayrollItemModel.id == item_id).first()

    def get_earnings(self, payroll_id: int):
        return self.db.query(PayrollItemModel).filter(
            PayrollItemModel.payroll_id == payroll_id,
            PayrollItemModel.item_type == "EARNING"
        ).all()

    def get_deductions(self, payroll_id: int):
        return self.db.query(PayrollItemModel).filter(
            PayrollItemModel.payroll_id == payroll_id,
            PayrollItemModel.item_type == "DEDUCTION"
        ).all()
    

    def create_payroll_item(self, payroll_item: PayrollItem) -> PayrollItem:

        new_payroll_item = to_model(payroll_item, PayrollItemModel)

        self.db.add(new_payroll_item)
        self.db.commit()
        self.db.refresh(new_payroll_item)

        return to_entity(new_payroll_item, PayrollItem)
