from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.domain.role import Role
from app.infrastructure.database import Base


# Modelo ORM
class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


# Repositorio
class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Role]:
        results = self.db.query(RoleModel).all()
        return [
            Role(
                id=row.id,
                name=row.name,
                description=row.description,
                created_at=row.created_at,
            )
            for row in results
        ]
