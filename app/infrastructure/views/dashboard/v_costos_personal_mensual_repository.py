from sqlalchemy import Column, String, Float
from app.infrastructure.database import Base
from sqlalchemy.orm import Session
from sqlalchemy import text

class VCostosPersonalMensualModel(Base):
    __tablename__ = "v_costos_personal_mensual"

    periodo = Column(String(7), primary_key=True)  # Ejemplo: "2025-10"
    total_pagado = Column(Float)
    total_descuentos = Column(Float)
    total_ingresos = Column(Float)


class VCostosPersonalMensualRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_costos_personal_mensual(self):
        """Retorna los costos de personal agrupados por mes"""
        return self.db.query(VCostosPersonalMensualModel).all()