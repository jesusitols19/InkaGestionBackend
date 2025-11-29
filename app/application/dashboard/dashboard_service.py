from app.infrastructure.views.dashboard.v_costos_personal_mensual_repository import VCostosPersonalMensualRepository
from app.infrastructure.views.dashboard.v_eficiencia_general_hoy_repository import VEficienciaGeneralHoyRepository
from app.infrastructure.views.dashboard.v_gasto_personal_total_repository import VGastoPersonalTotalRepository
from app.infrastructure.views.dashboard.v_horas_trabajadas_total_general_repository import VHorasTrabajadasTotalGeneralRepository
from app.infrastructure.views.dashboard.v_promedio_horas_hoy_repository import VPromedioHorasHoyRepository
from app.infrastructure.views.dashboard.v_total_empleados_repository import VTotalEmpleadosRepository
from app.infrastructure.views.dashboard.v_pagos_pendientes_repository import VPagosPendientesRepository
from app.infrastructure.views.dashboard.v_resumen_asistencia_hoy_repository import VResumenAsistenciaHoyRepository
# Nuevo repo
from app.infrastructure.views.dashboard.v_bi_analytics_repository import VBiAnalyticsRepository
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
            vResumenAsistenciaHoyRepository: VResumenAsistenciaHoyRepository,
            vBiAnalyticsRepository: VBiAnalyticsRepository): # <--- Inyección nueva
        
        self.vCostosPersonalMensualRepository = vCostosPersonalMensualRepository
        self.vEficienciaGeneralHoyRepository = vEficienciaGeneralHoyRepository
        self.vGastoPersonalTotalRepository = vGastoPersonalTotalRepository
        self.vHorasTrabajadasTotalGeneralRepository = vHorasTrabajadasTotalGeneralRepository
        self.vPromedioHorasHoyRepository = vPromedioHorasHoyRepository
        self.vTotalEmpleadosRepository = vTotalEmpleadosRepository
        self.vPagosPendientesRepository = vPagosPendientesRepository
        self.vResumenAsistenciaHoyRepository = vResumenAsistenciaHoyRepository
        self.vBiAnalyticsRepository = vBiAnalyticsRepository # <--- Asignación

    def get_full_dashboard(self):

        # --- 1. Obtener datos analíticos para Gráficos ---
        tendencia_data = self.vBiAnalyticsRepository.get_tendencia_asistencia()
        costos_area_data = self.vBiAnalyticsRepository.get_costos_por_area()
        top_extras_data = self.vBiAnalyticsRepository.get_top_horas_extra()

        # --- 2. Formatear datos para Gráficos (Listos para Chart.js/Recharts) ---
        
        # Gráfico Líneas: Asistencia diaria
        chart_asistencia = {
            "labels": [d.record_date.strftime('%d/%m') for d in tendencia_data],
            "dataset_a_tiempo": [d.total_a_tiempo for d in tendencia_data],
            "dataset_tardanza": [d.total_tardanzas for d in tendencia_data],
            "dataset_ausencia": [d.total_ausencias for d in tendencia_data]
        }

        # Gráfico Donut/Pastel: Costos por Área
        chart_costos = {
            "labels": [d.area_nombre for d in costos_area_data],
            "data": [d.total_pagado for d in costos_area_data]
        }

        # Gráfico Barras: Top Horas Extra
        chart_top_extras = {
            "labels": [d.nombre for d in top_extras_data],
            "data": [d.total_horas_extra for d in top_extras_data]
        }

        return jsend_success({
            # A. KPIs (Tarjetas Superiores - Tus datos originales)
            "kpis": {
                "total_empleados": self.vTotalEmpleadosRepository.get_total_empleados(),
                "eficiencia_general_hoy": self.vEficienciaGeneralHoyRepository.get_eficiencia_general_hoy(),
                "pagos_pendientes": self.vPagosPendientesRepository.get_pagos_pendientes(),
                "resumen_asistencia_hoy": self.vResumenAsistenciaHoyRepository.get_resumen_asistencia_hoy(),
                "gasto_personal_total": self.vGastoPersonalTotalRepository.get_gasto_personal_total(),
                "promedio_horas_hoy": self.vPromedioHorasHoyRepository.get_promedio_horas_hoy(),
                "horas_trabajadas_total_general": self.vHorasTrabajadasTotalGeneralRepository.get_horas_trabajadas_total_general(),
                "costos_personal_mensual": self.vCostosPersonalMensualRepository.get_costos_personal_mensual()
            },

            # B. GRÁFICOS (Business Intelligence - Nuevos)
            "charts": {
                "tendencia_asistencia": chart_asistencia,
                "distribucion_costos_area": chart_costos,
                "top_horas_extra": chart_top_extras
            }
        })