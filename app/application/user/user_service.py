import bcrypt
from app.infrastructure.user_repository import UserRepository
from app.infrastructure.user_repository import UserModel
from app.application.user.user_dto import UserUpdateDTO
from app.domain.user import User
from app.helpers.jsend_response import jsend_success
from app.helpers.jsend_response import jsend_fail
from typing import List

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def list_users(self) -> List[User]:

        list_users = self.repo.get_all()

        return jsend_success(list_users)
    
    def get_user_by_id(self, user_id:int):

        user = self.repo.find_by_id(user_id);
    
        if(user):
            return jsend_success(user)
        
        return jsend_fail({"message": "Usuario no encontrado"})

    def create_user(self, nombre: str, correo: str, password: str, role_id: int = 2):

        if self.repo.find_by_email(correo):
            return jsend_fail({"message": "Correo ya registrado"});
        
        salt = bcrypt.gensalt()
        
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

        user = UserModel(
            nombre=nombre,
            correo=correo,
            password_hash=hashed_password.decode("utf-8"),
            role_id=role_id
        )

        self.repo.create(user)

        return jsend_success({"message": "El usuario se creo correctamente"});

    def edit_user(self, user_id: int, dto: UserUpdateDTO) -> User:
        self.repo.update(user_id, dto)
        return jsend_success({"message": "El usuario fue editado correctamente"})
    
    
    def activate_user(self, user_id: int):
        if(self.repo.activate(user_id)):
            return jsend_success({"message": "El usuario fue activado correctamente"})
        return jsend_fail({"message": "usuario no encontrado"})
    
    def desactivate_user(self, user_id: int):

        if(self.repo.desactivate(user_id)):
            return jsend_success({"message": "El usuario fue desactivado correctamente"})
        return jsend_fail({"message": "usuario no encontrado"})