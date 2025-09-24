from fastapi import FastAPI
from app.presentation.role_routes import router as role_router
from app.presentation.employee_routes import router as employee_router

app = FastAPI()

# Incluimos las rutas
app.include_router(role_router)
app.include_router(employee_router)

