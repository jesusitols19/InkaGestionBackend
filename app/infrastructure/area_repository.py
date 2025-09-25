from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, TIMESTAMP, Date, ForeignKey, text
from app.infrastructure.database import Base



# Modelo ORM
class AreaModel(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120),nullable=False)
    code = Column(String(30),nullable=True)
    description = Column(String(255),nullable=True)
    active = Column(Boolean,nullable=False, server_default=text("TRUE") )
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))