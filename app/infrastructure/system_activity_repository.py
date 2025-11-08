from sqlalchemy.orm import Session
from sqlalchemy import Column, SmallInteger, Integer, String, Time, TIMESTAMP, text
from app.infrastructure.database import Base
from app.domain.systemactivity import SystemActivity
from app.helpers.orm_mapper import to_entity, to_model


class SystemActivityModel(Base):
    __tablename__ = "system_activity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    icono = Column(String(50), nullable=True, server_default=text("info"))
    created_by = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class SystemActivityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(SystemActivityModel).all()
    
    def add_system_activity(self, systemActivity:SystemActivity):
        model = to_model(systemActivity, SystemActivityModel)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return to_entity(model, SystemActivity)

