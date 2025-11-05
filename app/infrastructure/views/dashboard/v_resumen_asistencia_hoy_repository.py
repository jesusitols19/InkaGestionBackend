from sqlalchemy import Column, Float, Date, Integer
from app.infrastructure.database import Base
from sqlalchemy.orm import Session

class VResumenAsistenciaHoyModel(Base):
    __tablename__ = "v_resumen_asistencia_hoy"

    empleados_presentes = Column(Integer, primary_key=True)
    porcentaje_asistencia = Column(Float)


class VResumenAsistenciaHoyRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_resumen_asistencia_hoy(self):
        return self.db.query(VResumenAsistenciaHoyModel).first()
