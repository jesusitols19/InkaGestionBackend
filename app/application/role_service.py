from app.infrastructure.role_repository import RoleRepository

class RoleService:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def list_roles(self):
        return self.repo.get_all()
