from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.application.employee.employee_service import EmployeeService
from app.application.employee.employee_dto import EmployeeFilterDTO
from app.application.employee.employee_dto import EmployeeCreateDTO
from app.application.employee.employee_dto import EmployeeUpdateDTO
from app.infrastructure.employee_repository import EmployeeRepository
from app.helpers.jsend_response import jsend_success
from app.infrastructure.database import get_db
from app.dependencies import get_employee_service

router = APIRouter()

@router.get("/list-employees")
def list_employees(db:Session = Depends(get_db)):
    service = get_employee_service(db)
    response = service.list_employees();
    return response

@router.get("/search-employee")
def search_employees(
    filters: EmployeeFilterDTO = Depends(),   # ✅ FastAPI llena el DTO con los query params
    db: Session = Depends(get_db)
): 
    service = get_employee_service(db)
    response = service.buscar_empleados(filters)
    return response

@router.get("/search-employee-by-id/{employee_id}")
def search_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    service = get_employee_service(db)
    response = service.buscar_empleado_por_id(employee_id)
    return response

@router.post("/create-employee")
def create_employee(dto: EmployeeCreateDTO, db: Session = Depends(get_db)):
    service = get_employee_service(db)
    response = service.crear_empleado(dto)
    return response

@router.put("/update-employee/{employee_id}")
def update_employee(employee_id: int, dto: EmployeeUpdateDTO, db: Session = Depends(get_db)):
    service = get_employee_service(db)
    response = service.editar_empleado(employee_id, dto)
    return response

@router.put("/activate-employee/{employee_id}")
def activate_employee(employee_id:int, db:Session = Depends(get_db)):
    service = get_employee_service(db)
    response = service.activar_empleado(employee_id)
    return response


@router.delete("/delete-employee/{employee_id}")
def desactivate_employee(employee_id: int, db: Session = Depends(get_db)):
    service = get_employee_service(db)
    response = service.desactivar_empleado(employee_id)
    return response