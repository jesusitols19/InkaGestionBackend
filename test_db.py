from sqlalchemy import create_engine, text
from app.shared.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.fetchone())
