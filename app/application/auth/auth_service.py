import bcrypt
from app.infrastructure.user_repository import UserRepository
from app.helpers.jsend_response import jsend_success
from app.helpers.jsend_response import jsend_fail

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def login(self, email: str, password: str):

        user = self.repo.find_by_email(email)

        if not user or not user.active:
            return jsend_fail({"message": "Credenciales invalidas"})

        # comparar hash
        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return jsend_fail({"message": "credenciales invalidas"})

        # actualizar last_login
        self.repo.update_last_login(user)

        return jsend_success({
            "id": user.id,
            "nombre": user.nombre,
            "correo": user.correo,
        })
