from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.shared.config import DATABASE_URL

# Motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

# Fábrica de sesiones
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base para los modelos
Base = declarative_base()

# Dependencia de FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
