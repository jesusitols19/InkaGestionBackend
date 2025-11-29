from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

#from app.scheduler.schedulers.background import BackgroundScheduler
from app.infrastructure.database import SessionLocal
from app.infrastructure.scheduled_reports_repository import ScheduledReportRepository
from app.application.scheduledreport.scheduled_reports_service import ScheduledReportService

from app.presentation.role_routes import router as role_router
from app.presentation.employee_routes import router as employee_router
from app.presentation.auth_routes import router as auth_router
from app.presentation.user_routes import router as user_router
from app.presentation.attendance_record_routes import router as attendance_record_router
from app.presentation.payroll_periods_routes import router as payroll_period_router
from app.presentation.payroll_routes import router as payroll_router
from app.presentation.shift_routes import router as shift_router
from app.presentation.employee_shift_routes import router as employee_shif_router
from app.presentation.payment_run_routes import router as payment_run_router
from app.presentation.advance_routes import router as advance_router
from app.presentation.dashboard_routes import router as dashboard_router
from app.presentation.system_activity_routes import router as system_activity_router
from app.presentation.scheduled_report_routes import router as scheduled_report_router
from app.helpers.jsend_response import jsend_error
from app.presentation.area_routes import router as area_router
from app.presentation.ia_routes import router as ia_router

app = FastAPI()

origins = [
    "http://localhost:4200",   # Angular dev server
    "http://127.0.0.1:4200",   # por si usas esta URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # aquí defines qué frontends pueden acceder
    allow_credentials=True,
    allow_methods=["*"],            # puedes restringir si quieres solo POST/GET
    allow_headers=["*"],            # permite cualquier cabecera
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=jsend_error("Error interno del servidor", data=str(exc))
    )

# Incluimos las rutas
app.include_router(role_router)
app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(attendance_record_router)
app.include_router(payroll_period_router)
app.include_router(payroll_router)
app.include_router(shift_router)
app.include_router(employee_shif_router)
app.include_router(payment_run_router)
app.include_router(advance_router)
app.include_router(dashboard_router)
app.include_router(system_activity_router)
app.include_router(scheduled_report_router)
app.include_router(area_router)
app.include_router(ia_router, prefix="/api/v1/ia", tags=["Inteligencia Artificial"])

# def run_scheduled_reports():
#     db = SessionLocal()
#     try:
#         repo = ScheduledReportRepository(db)
#         service = ScheduledReportService(repo)
#         print("Ejecutando tarea programada de reportes...")

#         asyncio.run(service.execute_due_reports())

#         db.commit()
#     except Exception as e:
#         print(f"Error al ejecutar reportes programados: {e}")
#     finally:
#         db.close()


# scheduler = BackgroundScheduler()
# scheduler.add_job(run_scheduled_reports, 'interval', minutes=60)
# scheduler.start()

# @app.on_event("shutdown")
# def shutdown_event():
#     scheduler.shutdown()


