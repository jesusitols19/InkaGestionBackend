from sqlalchemy import Column, Integer
from app.infrastructure.database import Base
from sqlalchemy.orm import Session

class VTotalEmpleadosModel(Base):
    __tablename__ = "v_total_empleados"

    total_empleados = Column(Integer, primary_key=True)


class VTotalEmpleadosRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_total_empleados(self):
        """Retorna la cantidad total de empleados activos"""
        return self.db.query(VTotalEmpleadosModel).first()