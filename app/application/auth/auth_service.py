import bcrypt
from app.infrastructure.user_repository import UserRepository
from app.helpers.jsend_response import jsend_success
from app.helpers.jsend_response import jsend_fail

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def login(self, email: str, password: str):

        user = self.repo.find_by_email(email)

        if not user:
            return jsend_fail({"message": "Credenciales invalidas"})

        if not user.active:
            return jsend_fail({"message": "Usuario bloqueado. Por favor, contacte al administrador."})

        # comparar hash
        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            self.repo.increment_failed_login_attempts(user)
            
            if user.failed_login_attempts >= 5:
                self.repo.deactivate_user(user)
                return jsend_fail({"message": "Usuario bloqueado por multiples intentos fallidos."})
            
            return jsend_fail({"message": "Credenciales invalidas"})

        # Si el login es exitoso, reseteamos el contador
        if user.failed_login_attempts > 0:
            self.repo.reset_failed_login_attempts(user)

        # actualizar last_login
        self.repo.update_last_login(user)

        return jsend_success({
            "id": user.id,
            "nombre": user.nombre,
            "correo": user.correo,
        })
