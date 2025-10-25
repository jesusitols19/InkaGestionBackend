from app.infrastructure.payroll_periods_repository import PayrollPeriodRepository
from app.domain.payrollperiods import PayrollPeriod
from app.application.payrollperiods.payroll_periods_dto import PayrollPeriodCreateDTO, PayrollPeriodUpdateDTO
from app.helpers.orm_mapper import to_entity, to_model


class PayrollPeriodService:
    def __init__(self, repo: PayrollPeriodRepository):
        self.repo = repo

    def get_all_periods(self):
        return self.repo.get_all()

    def get_period_by_id(self, period_id: int):
        return self.repo.find_by_id(period_id)

    def get_open_period(self):
        return self.repo.find_open_period()

    def create_payroll_period(self, dto: PayrollPeriodCreateDTO) -> PayrollPeriod:
        entity = PayrollPeriod(**dto.__dict__)
        return self.repo.create_payroll_period(entity)

    def update_payroll_period(self, dto: PayrollPeriodUpdateDTO) -> PayrollPeriod:
        entity = PayrollPeriod(**dto.__dict__)
        return self.repo.update_payroll_period(entity)