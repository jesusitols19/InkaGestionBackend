from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, TIMESTAMP, Date, ForeignKey, text
from app.domain.employee import Employee
from app.infrastructure.database import Base
from typing import Optional

# Modelo ORM
class EmployeeModel(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_number = Column(String(50), unique=True, nullable=True)
    nombre = Column(String(150), nullable=False)
    documento = Column(String(50), nullable=True)
    correo = Column(String(150), nullable=True)
    telefono = Column(String(50), nullable=True)
    area_id = Column(Integer, ForeignKey("areas.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    hire_date = Column(Date, nullable=True)
    salary_base = Column(DECIMAL(12, 2), nullable=False, server_default=text("0.00"))
    contract_type = Column(String(60), nullable=True)
    bank_account = Column(String(120), nullable=True)
    active = Column(Boolean, nullable=False, server_default=text("TRUE"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)

# Repositorio
class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Employee]:
        results = self.db.query(EmployeeModel).all()
        return [self._map_to_entity(row) for row in results]
    
    def search(
        self,
        nombre: Optional[str] = None,
        documento: Optional[str] = None,
        telefono: Optional[str] = None,
        area_id: Optional[int] = None,
        salario_min: Optional[float] = None,
        salario_max: Optional[float] = None,
        solo_activos: Optional[bool] = None,
    ) -> list[Employee]:
        query = self.db.query(EmployeeModel)

        if nombre:
            query = query.filter(EmployeeModel.nombre.ilike(f"%{nombre}%"))
        if documento:
            query = query.filter(EmployeeModel.documento == documento)
        if telefono:
            query = query.filter(EmployeeModel.telefono == telefono)
        if area_id:
            query = query.filter(EmployeeModel.area_id == area_id)
        if salario_min is not None:
            query = query.filter(EmployeeModel.salary_base >= salario_min)
        if salario_max is not None:
            query = query.filter(EmployeeModel.salary_base <= salario_max)
        if solo_activos is not None:
            query = query.filter(EmployeeModel.active == solo_activos)

        results = query.all()
        return [self._map_to_entity(row) for row in results]
    

    
    def _map_to_entity(self, row: EmployeeModel) -> Employee:
        return Employee(
            id=row.id,
            employee_number=row.employee_number,
            nombre=row.nombre,
            documento=row.documento,
            correo=row.correo,
            telefono=row.telefono,
            area_id=row.area_id,
            hire_date=row.hire_date,
            salary_base=row.salary_base,
            contract_type=row.contract_type,
            bank_account=row.bank_account,
            active=row.active,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )