from sqlalchemy import Column, Integer
from app.infrastructure.database import Base
from sqlalchemy.orm import Session

class VPagosPendientesModel(Base):
    __tablename__ = "v_pagos_pendientes"

    pagos_pendientes = Column(Integer, primary_key=True)


class VPagosPendientesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_pagos_pendientes(self):
        
        return self.db.query(VPagosPendientesModel).first()