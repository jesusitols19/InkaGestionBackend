from fastapi import FastAPI
from app.presentation.role_routes import router as role_router

app = FastAPI()

# Incluimos las rutas
app.include_router(role_router)

