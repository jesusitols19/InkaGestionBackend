from sqlalchemy.orm import Session
from sqlalchemy import Column, SmallInteger, Integer, String, Time, TIMESTAMP, text
from app.infrastructure.database import Base

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
    
    