from sqlalchemy.orm import Session
from sqlalchemy import Column, SmallInteger, Integer, String, Time, TIMESTAMP, text
from app.infrastructure.database import Base
from app.domain.shift import Shift
from app.helpers.orm_mapper import to_entity, to_model

# Modelo ORM

class ShiftModel(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    tolerance_minutes = Column(SmallInteger, nullable=False, server_default=text("0"))
    description = Column(String(255), nullable=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


# Repositorio
class ShiftRepository:
    def __init__(self, db: Session):
        self.db = db


    def get_shift_by_id(self, shift_id: int) -> ShiftModel:
        return self.db.query(ShiftModel).filter(ShiftModel.id == shift_id).first()
    

    def get_all_shifts(self) -> list[Shift]:
        shift_models = self.db.query(ShiftModel).all()
        return [to_entity(shift_model, Shift) for shift_model in shift_models]

    def create_shift(self, shift: Shift) -> Shift:

        new_shift = to_model(shift, ShiftModel)

        self.db.add(new_shift)
        self.db.commit()
        self.db.refresh(new_shift)

        return to_entity(new_shift, Shift)
    
    