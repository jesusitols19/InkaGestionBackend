from app.infrastructure.employee_repository import EmployeeRepository
from app.infrastructure.area_repository import AreaRepository
from app.application.employee.employee_dto import EmployeeFilterDTO
from app.application.employee.employee_dto import EmployeeCreateDTO
from app.application.employee.employee_dto import EmployeeUpdateDTO
from app.helpers.jsend_response import jsend_success
from app.helpers.jsend_response import jsend_fail
from app.domain.employee import Employee
from typing import List

class EmployeeService:

    def __init__(self, repo: EmployeeRepository, area_repo: AreaRepository):
        self.repo = repo
        self.area_repo = area_repo

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
    
    def buscar_empleado_por_id(self, employee_id: int) -> Employee:

        empleado = self.repo.find_by_employee_id(employee_id)

        if not empleado:
            return jsend_fail({"message": "Empleado no encontrado"})
        
        area = self.area_repo.find_by_area_id(empleado.area_id)

        area_name = area.name if area else None

        empleado_dict = {
            "id": empleado.id,
            "nombre": empleado.nombre,
            "correo": empleado.correo,
            "employee_number": empleado.employee_number,
            "telefono": empleado.telefono,
            "hire_date": empleado.hire_date,
            "contract_type": empleado.contract_type,
            "salary_base": empleado.salary_base,
            "bank_account": empleado.bank_account,
            "documento": empleado.documento,
            "active": empleado.active,
            "created_at": empleado.created_at,
            "updated_at": empleado.updated_at,
            "area": {
                "id": empleado.area_id,
                "name": area_name
            }
        }


        return jsend_success(empleado_dict)

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


