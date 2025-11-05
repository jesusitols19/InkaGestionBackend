from sqlalchemy import Column, Float, Integer, DateTime
from app.infrastructure.database import Base
from sqlalchemy.orm import Session


class VGastoPersonalTotalModel(Base):
    __tablename__ = "v_gasto_personal_total"

    gasto_total_personal = Column(Float)
    total_empleados = Column(Integer)
    fecha_actual = Column(DateTime, primary_key=True)


class VGastoPersonalTotalRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_gasto_personal_total(self):
        """Gasto total en sueldos base del personal activo"""
        return self.db.query(VGastoPersonalTotalModel).first()