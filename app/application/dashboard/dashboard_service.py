from app.infrastructure.views.dashboard.v_costos_personal_mensual_repository import VCostosPersonalMensualRepository
from app.infrastructure.views.dashboard.v_eficiencia_general_hoy_repository import VEficienciaGeneralHoyRepository
from app.infrastructure.views.dashboard.v_gasto_personal_total_repository import VGastoPersonalTotalRepository
from app.infrastructure.views.dashboard.v_horas_trabajadas_total_general_repository import VHorasTrabajadasTotalGeneralRepository
from app.infrastructure.views.dashboard.v_promedio_horas_hoy_repository import VPromedioHorasHoyRepository
from app.infrastructure.views.dashboard.v_total_empleados_repository import VTotalEmpleadosRepository
from app.infrastructure.views.dashboard.v_pagos_pendientes_repository import VPagosPendientesRepository
from app.infrastructure.views.dashboard.v_resumen_asistencia_hoy_repository import VResumenAsistenciaHoyRepository
from app.helpers.jsend_response import jsend_success


class DashboardService:

    def __init__(
            self,
            vCostosPersonalMensualRepository: VCostosPersonalMensualRepository,
            vEficienciaGeneralHoyRepository: VEficienciaGeneralHoyRepository,
            vGastoPersonalTotalRepository:VGastoPersonalTotalRepository,
            vHorasTrabajadasTotalGeneralRepository:VHorasTrabajadasTotalGeneralRepository,
            vPromedioHorasHoyRepository:VPromedioHorasHoyRepository,
            vTotalEmpleadosRepository:VTotalEmpleadosRepository,
            vPagosPendientesRepository:VPagosPendientesRepository,
            vResumenAsistenciaHoyRepository: VResumenAsistenciaHoyRepository):
        
        self.vCostosPersonalMensualRepository = vCostosPersonalMensualRepository
        self.vEficienciaGeneralHoyRepository = vEficienciaGeneralHoyRepository
        self.vGastoPersonalTotalRepository = vGastoPersonalTotalRepository
        self.vHorasTrabajadasTotalGeneralRepository = vHorasTrabajadasTotalGeneralRepository
        self.vPromedioHorasHoyRepository = vPromedioHorasHoyRepository
        self.vTotalEmpleadosRepository = vTotalEmpleadosRepository
        self.vPagosPendientesRepository = vPagosPendientesRepository
        self.vResumenAsistenciaHoyRepository = vResumenAsistenciaHoyRepository

    def get_full_dashboard(self):

        return jsend_success({
            "costos_personal_mensual": self.vCostosPersonalMensualRepository.get_costos_personal_mensual(),
            "total_empleados": self.vTotalEmpleadosRepository.get_total_empleados(),
            "horas_trabajadas_total_general": self.vHorasTrabajadasTotalGeneralRepository.get_horas_trabajadas_total_general(),
            "promedio_horas_hoy": self.vPromedioHorasHoyRepository.get_promedio_horas_hoy(),
            "eficiencia_general_hoy": self.vEficienciaGeneralHoyRepository.get_eficiencia_general_hoy(),
            "gasto_personal_total": self.vGastoPersonalTotalRepository.get_gasto_personal_total(),
            "pagos_pendientes": self.vPagosPendientesRepository.get_pagos_pendientes(),
            "resumen_asistencia_hoy": self.vResumenAsistenciaHoyRepository.get_resumen_asistencia_hoy()
        })


