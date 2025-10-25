from app.infrastructure.advances_repository import AdvanceRepository
from app.application.advance.advance_dto import AdvanceRequestDTO, AdvanceApproveDTO
from app.domain.advances import Advance
from app.helpers.jsend_response import jsend_success, jsend_fail
from datetime import datetime


class AdvanceService:
    def __init__(self, repo: AdvanceRepository):
        self.repo = repo


    def request_advance(self, dto : AdvanceRequestDTO):
        entity = Advance(**dto.__dict__)
        return jsend_success(self.repo.request_advance(entity))
    
    def approve_advance(self, dto : AdvanceApproveDTO):

        advance = self.repo.find_by_id(dto.advance_id)

        if not advance or advance.status != "PENDING":
            return jsend_fail("No existe el adelanto")
        
        advance.status = "APPROVED" if dto.approve else "REJECTED"

        advance.approved_by = dto.approved_by

        advance.approved_at = datetime.now()

        return jsend_success(self.repo.update_advance(advance))
    
    def mark_paid(self, advance_id: int):

        advance = self.repo.find_by_id(advance_id)

        if not advance or advance.status == "APPROVED":
            advance.status = "PAID"
            return jsend_success(self.repo.update_advance(advance))
        
        return jsend_fail("El adelanto todavia no fue aprobada")



