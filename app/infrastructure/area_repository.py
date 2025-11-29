from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, TIMESTAMP, Date, ForeignKey, text
from app.infrastructure.database import Base
from app.domain.area import Area


# Modelo ORM
class AreaModel(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120),nullable=False)
    code = Column(String(30),nullable=True)
    description = Column(String(255),nullable=True)
    active = Column(Boolean,nullable=False, server_default=text("TRUE") )
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class AreaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Area]:
        results = self.db.query(AreaModel).filter(AreaModel.active == True).all()
        return [
            Area(
                id=row.id,
                name=row.name,
                code=row.code,
                description=row.description,
                active=row.active,
                created_at=row.created_at
            ) for row in results
        ]

    def find_by_area_id(self, area_id: int):
        return self.db.query(AreaModel).filter(AreaModel.id == area_id).first()