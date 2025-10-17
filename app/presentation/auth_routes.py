from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.user_repository import UserRepository
from app.application.auth.auth_service import AuthService
from app.application.auth.auth_dto import AuthLogin

router = APIRouter()

@router.post("/login")
def login(credential: AuthLogin, db: Session = Depends(get_db)):

    repo = UserRepository(db)
    service = AuthService(repo)
    response = service.login(
        credential.email,
        credential.password
    )

    return response
