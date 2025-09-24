from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.application.employee.employee_service import EmployeeService
from app.application.employee.employee_dto import EmployeeFilterDTO
from app.infrastructure.employee_repository import EmployeeRepository
from app.infrastructure.database import get_db

router = APIRouter()

@router.get("/list-employees")
def list_employees(db:Session = Depends(get_db)):
    repo = EmployeeRepository(db);
    service = EmployeeService(repo);
    empleados = service.list_employees();
    return empleados

@router.get("/search-employee")
def search_employees(
    filters: EmployeeFilterDTO = Depends(),   # ✅ FastAPI llena el DTO con los query params
    db: Session = Depends(get_db)
): 
    repo = EmployeeRepository(db)
    service = EmployeeService(repo)
    empleados = service.buscar_empleados(filters)
    return empleados