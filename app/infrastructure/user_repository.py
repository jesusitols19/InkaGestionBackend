from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, TIMESTAMP, text
from sqlalchemy.orm import relationship, Session
from app.infrastructure.database import Base
from app.domain.user import User

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    correo = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    active = Column(Boolean, nullable=False, server_default=text("TRUE"))
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, default=2)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[User]:
        results = self.db.query(UserModel).all()
        return [self._map_to_entity(row) for row in results]
    
    def find_by_id(self, id: int):
        return self.db.query(UserModel).filter(UserModel.id == id).first()

    def find_by_email(self, email: str):
        return self.db.query(UserModel).filter(UserModel.correo == email).first()
    
    def create(self, user: UserModel):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user_id: int, dto) -> User:
        usuario = self.db.query(UserModel).filter(UserModel.id == user_id).first()

        # if not usuario:
        #     raise HTTPException(status_code=404, detail="Empleado no encontrado")

        # Actualizar solo los campos enviados en el DTO
        for field, value in dto.dict(exclude_unset=True).items():
            setattr(usuario, field, value)

        self.db.commit()
        self.db.refresh(usuario)

        return self._map_to_entity(usuario)

    def update_last_login(self, user: UserModel):
        from datetime import datetime
        user.last_login = datetime.now()
        self.db.add(user)
        self.db.commit()
        return user
    

    def activate(self, user_id: int):
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            return False
        
        user.active = True

        self.db.commit()
        self.db.refresh(user)
        return True
    
    def desactivate(self, user_id: int):
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            return False

        user.active = False

        self.db.commit()
        self.db.refresh(user)
        return True
    
    def _map_to_entity(self, row: UserModel) -> User:
        return User(
            id=row.id,
            nombre=row.nombre,
            correo=row.correo,
            role_id=row.role_id,
            password_hash=row.password_hash,
            active=row.active,
            last_login=row.last_login,
            created_at=row.created_at,
            updated_at=row.updated_at
        )

