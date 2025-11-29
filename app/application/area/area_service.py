from app.infrastructure.area_repository import AreaRepository
from app.helpers.jsend_response import jsend_success

class AreaService:
    def __init__(self, repo: AreaRepository):
        self.repo = repo

    def get_all_areas(self):
        areas = self.repo.get_all()
        return jsend_success(areas)