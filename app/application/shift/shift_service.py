from app.infrastructure.shift_repository import ShiftRepository
from app.application.shift.shift_dto import ShiftCreateDTO
from app.domain.shift import Shift
from app.helpers.jsend_response import jsend_success, jsend_fail


class ShiftService:

    def __init__(self, repo: ShiftRepository):
        self.repo = repo


    def get_all_shift(self):
        return jsend_success(self.repo.get_all_shifts())

    def create_shift(self, dto : ShiftCreateDTO) -> Shift:

        entity = Shift(**dto.__dict__)

        return jsend_success(self.repo.create_shift(entity))

        
