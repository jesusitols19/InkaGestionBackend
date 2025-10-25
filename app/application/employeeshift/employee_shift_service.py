from app.infrastructure.employee_shift_repository import EmployeeShiftRepository
from app.application.employeeshift.employee_shift_dto import EmployeeShiftCreateDTO
from app.domain.employeeshift import EmployeeShift
from app.helpers.jsend_response import jsend_success, jsend_fail

class EmployeeShiftService:

    def __init__(self, repo: EmployeeShiftRepository):
        self.repo = repo


    def create_employee_shift(self, dto : EmployeeShiftCreateDTO) -> EmployeeShift:
        entity = EmployeeShift(**dto.__dict__)
        return jsend_success(self.repo.assign_shift_to_employee(entity))
    
    def get_all_employee_shift(self):
        return jsend_success(self.repo.get_all_employee_shifts())