from sqlalchemy import Column, Float, Date
from app.infrastructure.database import Base
from sqlalchemy.orm import Session

class VPromedioHorasHoyModel(Base):
    __tablename__ = "v_promedio_horas_hoy"

    fecha_actual = Column(Date, primary_key=True)
    promedio_horas_hoy = Column(Float)

class VPromedioHorasHoyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_promedio_horas_hoy(self):
        """Promedio de horas trabajadas el día actual"""
        return self.db.query(VPromedioHorasHoyModel).first()