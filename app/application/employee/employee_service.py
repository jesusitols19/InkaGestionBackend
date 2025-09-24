from app.infrastructure.employee_repository import EmployeeRepository
from app.application.employee.employee_dto import EmployeeFilterDTO
from app.domain.employee import Employee
from typing import List

class EmployeeService:

    def __init__(self, repo: EmployeeRepository):
        self.repo = repo
    
    def list_employees(self) -> List[Employee]:
        return self.repo.get_all();

    def buscar_empleados(self, filters: EmployeeFilterDTO) -> List[Employee]:
        return self.repo.search(
            nombre=filters.nombre,
            documento=filters.documento,
            telefono=filters.telefono,
            area_id=filters.area_id,
            salario_min=filters.salario_min,
            salario_max=filters.salario_max,
            solo_activos=filters.solo_activos,
        )

