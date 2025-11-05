from sqlalchemy import Column, Float, Date
from app.infrastructure.database import Base
from sqlalchemy.orm import Session

class VEficienciaGeneralHoyModel(Base):
    __tablename__ = "v_eficiencia_general_hoy"

    fecha_actual = Column(Date, primary_key=True)
    eficiencia_general_porcentaje = Column(Float)

class VEficienciaGeneralHoyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_eficiencia_general_hoy(self):
        """Porcentaje de empleados presentes hoy"""
        return self.db.query(VEficienciaGeneralHoyModel).first()
