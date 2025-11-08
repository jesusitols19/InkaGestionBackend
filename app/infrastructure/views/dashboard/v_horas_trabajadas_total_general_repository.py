from sqlalchemy import Column, String, Float
from app.infrastructure.database import Base
from sqlalchemy.orm import Session

class VHorasTrabajadasTotalGeneralModel(Base):
    __tablename__ = "v_horas_trabajadas_total_general"

    mes = Column(String(7), primary_key=True)
    total_horas_trabajadas = Column(Float)
    total_horas_extra = Column(Float)
    total_general = Column(Float)

class VHorasTrabajadasTotalGeneralRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_horas_trabajadas_total_general(self):
        """Retorna las horas totales trabajadas y extra del mes actual"""
        return self.db.query(VHorasTrabajadasTotalGeneralModel).first()