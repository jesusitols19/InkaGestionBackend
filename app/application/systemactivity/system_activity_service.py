from app.infrastructure.system_activity_repository import SystemActivityRepository
from app.helpers.jsend_response import jsend_success
from app.domain.systemactivity import SystemActivity
from app.application.systemactivity.system_activity_dto import SystemActivityCreateDTO

class SystemActivityService:

    def __init__(self, repo:SystemActivityRepository):
        self.repo = repo

    def get_all(self):
        return jsend_success(self.repo.get_all())
    
    def add_system_activity(self, dto:SystemActivityCreateDTO):
        new_entity = SystemActivity(**dto.__dict__)
        return jsend_success(self.repo.add_system_activity(new_entity))