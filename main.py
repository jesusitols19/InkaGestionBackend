from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.presentation.role_routes import router as role_router
from app.presentation.employee_routes import router as employee_router
from app.helpers.jsend_response import jsend_error

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=jsend_error("Error interno del servidor", data=str(exc))
    )

# Incluimos las rutas
app.include_router(role_router)
app.include_router(employee_router)

