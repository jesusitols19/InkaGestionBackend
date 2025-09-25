from app.infrastructure.employee_repository import EmployeeRepository
from app.application.employee.employee_dto import EmployeeFilterDTO
from app.application.employee.employee_dto import EmployeeCreateDTO
from app.application.employee.employee_dto import EmployeeUpdateDTO
from app.helpers.jsend_response import jsend_success
from app.helpers.jsend_response import jsend_fail
from app.domain.employee import Employee
from typing import List

class EmployeeService:

    def __init__(self, repo: EmployeeRepository):
        self.repo = repo
    
    def list_employees(self) -> List[Employee]:

        list_employees = self.repo.get_all()

        return jsend_success(list_employees)

    def buscar_empleados(self, filters: EmployeeFilterDTO) -> List[Employee]:

        list_employees = self.repo.search(
            nombre=filters.nombre,
            documento=filters.documento,
            telefono=filters.telefono,
            area_id=filters.area_id,
            salario_min=filters.salario_min,
            salario_max=filters.salario_max,
            solo_activos=filters.solo_activos,
        )

        return jsend_success(list_employees)

    def crear_empleado(self, dto: EmployeeCreateDTO) -> Employee:

        existente = self.repo.find_by_employee_number(dto.employee_number)

        if existente:
            return jsend_fail({"message": "Ya existe un empleado con este documento"})
        
        self.repo.create(dto)

        return jsend_success({"message": "El empleado fue creado correctamente"})
    

    def editar_empleado(self, employee_id: int, dto: EmployeeUpdateDTO) -> Employee:
        self.repo.update(employee_id, dto)
        return jsend_success({"message": "El empleado fue editado correctamente"})
    
    
    def activar_empleado(self, employee_id: int):
        if(self.repo.activate(employee_id)):
            return jsend_success({"message": "El empleado fue activado correctamente"})
        return jsend_fail({"message": "Empleado no encontrado"})
    
    def desactivar_empleado(self, employee_id: int):

        if(self.repo.desactivate(employee_id)):
            return jsend_success({"message": "El empleado fue desactivado correctamente"})
        return jsend_fail({"message": "Empleado no encontrado"})


