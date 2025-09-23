from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.application.role_service import RoleService
from app.infrastructure.role_repository import RoleRepository
from app.infrastructure.database import get_db

router = APIRouter()


@router.get("/roles")
def list_roles(db: Session = Depends(get_db)):
    repo = RoleRepository(db)   # ✅ aquí pasamos la sesión
    service = RoleService(repo)
    return service.list_roles()