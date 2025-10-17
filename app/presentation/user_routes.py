from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.user_repository import UserRepository
from app.application.user.user_service import UserService
from app.application.user.user_dto import UserCreate
from app.application.user.user_dto import UserUpdateDTO

router = APIRouter()

@router.get("/list-users")
def list_users(db:Session = Depends(get_db)):

    repo = UserRepository(db);
    service = UserService(repo);
    response = service.list_users();

    return response


@router.get("/get-user-by-id/{user_id}")
def list_users(user_id: int, db:Session = Depends(get_db)):

    repo = UserRepository(db);
    service = UserService(repo);
    response = service.get_user_by_id(user_id);

    return response


@router.post("/create-user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    repo = UserRepository(db)
    service = UserService(repo)
    response = service.create_user(
        user.nombre,
        user.correo,
        user.password,
        user.role_id
    )
    
    return response


@router.put("/update-user/{user_id}")
def update_employee(user_id: int, dto: UserUpdateDTO, db: Session = Depends(get_db)):

    repo = UserRepository(db)
    service = UserService(repo)
    response = service.edit_user(user_id, dto)

    return response


@router.put("/activate-user/{user_id}")
def activate_employee(user_id:int, db:Session = Depends(get_db)):

    repo = UserRepository(db)
    service = UserService(repo)
    response = service.activate_user(user_id)

    return response


@router.delete("/delete-user/{user_id}")
def desactivate_employee(user_id: int, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)
    response = service.desactivate_user(user_id)
    return response
