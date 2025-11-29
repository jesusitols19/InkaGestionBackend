from sqlalchemy import Column, String, Float, Integer, Date
from app.infrastructure.database import Base
from sqlalchemy.orm import Session

# --- MODELOS ORM (Mapean a las vistas SQL nuevas) ---

class VBiAsistenciaTendenciaModel(Base):
    __tablename__ = "v_bi_asistencia_tendencia"
    record_date = Column(Date, primary_key=True)
    total_a_tiempo = Column(Integer)
    total_tardanzas = Column(Integer)
    total_ausencias = Column(Integer)

class VBiCostosPorAreaModel(Base):
    __tablename__ = "v_bi_costos_por_area"
    area_nombre = Column(String, primary_key=True)
    total_pagado = Column(Float)

class VBiTopHorasExtraModel(Base):
    __tablename__ = "v_bi_top_horas_extra"
    nombre = Column(String, primary_key=True)
    total_horas_extra = Column(Float)

# --- CLASE REPOSITORIO ---

class VBiAnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_tendencia_asistencia(self):
        """Devuelve datos históricos para gráficos de líneas"""
        return self.db.query(VBiAsistenciaTendenciaModel).order_by(VBiAsistenciaTendenciaModel.record_date).all()

    def get_costos_por_area(self):
        """Devuelve datos para gráficos de torta/pastel"""
        return self.db.query(VBiCostosPorAreaModel).all()

    def get_top_horas_extra(self):
        """Devuelve el ranking de empleados con más horas extra"""
        return self.db.query(VBiTopHorasExtraModel).order_by(VBiTopHorasExtraModel.total_horas_extra.desc()).all()