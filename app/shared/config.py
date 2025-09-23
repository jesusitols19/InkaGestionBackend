import os
from dotenv import load_dotenv


load_dotenv()  # Carga variables de .env


# Ejemplo de conexion: mysql+mysqlconnector://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BASE_DATOS


# Sin .env
# DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:jesusitols19@127.0.0.1:3306/inkaperu")

# Con .env
DATABASE_URL = os.getenv("DATABASE_URL")