import pandas as pd
import numpy as np
import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# --- LIBRERÍAS DE IA (SCIKIT-LEARN) ---
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, r2_score, silhouette_score # <--- NUEVAS MÉTRICAS IMPORTADAS
from sklearn.ensemble import IsolationForest

# --- LIBRERÍAS PARA EXCEL ---
from pandas import ExcelWriter
from openpyxl.styles import Font, Alignment
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import get_column_letter

# --- DEPENDENCIAS DEL PROYECTO ---
from app.dependencies import get_db
from app.helpers.jsend_response import jsend_success, jsend_error

router = APIRouter()

def _formatear_hoja_excel(worksheet: Worksheet, currency_columns: list = []):
    """
    Aplica estilos profesionales a una hoja de cálculo.
    """
    header_font = Font(bold=True)
    for r_idx, row in enumerate(worksheet.iter_rows(), 1):
        for c_idx, cell in enumerate(row, 1):
            col_letter = get_column_letter(c_idx)
            if r_idx == 1:
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center")
            
            # Autoajuste de ancho (estimado)
            current_width = worksheet.column_dimensions[col_letter].width
            val_len = len(str(cell.value)) if cell.value else 0
            new_width = val_len * 1.2
            if new_width > (current_width or 10):
                worksheet.column_dimensions[col_letter].width = min(new_width, 50)
            
            # Formato moneda
            if r_idx > 1 and col_letter in currency_columns:
                cell.number_format = '"S/ "#,##0.00'

# ==============================================================================
# 1. PREDICCIÓN DE COSTOS (MEJORADA CON MÉTRICAS CIENTÍFICAS)
# ==============================================================================
@router.get("/predecir-costos-planilla", summary="REQ-35/36: Predicción Multivariable con Validación Estadística")
async def predecir_costos_planilla(db: Session = Depends(get_db)):
    try:
        # 1. Consulta SQL enriquecida (Tiempo + Carga Laboral)
        sql_query = """
            SELECT 
                p.start_date, 
                COUNT(pr.id) as num_empleados,
                SUM(pr.net_pay) as total_cost
            FROM payrolls pr
            JOIN payroll_periods p ON pr.period_id = p.id
            GROUP BY p.start_date, p.id
            ORDER BY p.start_date;
        """
        df = pd.read_sql(sql_query, db.bind)

        if df.empty or len(df) < 2:
            return jsend_success(data={
                "prediccion_costo_siguiente_periodo": 0,
                "nota": "Insuficientes datos históricos para entrenar el modelo."
            })

        # 2. Preparación de Datos (Feature Engineering)
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['dias_desde_inicio'] = (df['start_date'] - df['start_date'].min()).dt.days
        
        # X = Variables Independientes (Tiempo y Cantidad de Empleados)
        # y = Variable Dependiente (Costo Total)
        X = df[['dias_desde_inicio', 'num_empleados']]
        y = df['total_cost']

        # 3. Entrenamiento (Online Training)
        model = LinearRegression()
        model.fit(X, y)

        # 4. Validación del Modelo (Métricas de Calidad para tu Profesor)
        y_pred_historico = model.predict(X)
        r2 = r2_score(y, y_pred_historico)      # Coeficiente de Determinación
        mse = mean_squared_error(y, y_pred_historico) # Error Cuadrático Medio

        # 5. Predicción Futura
        dias_siguiente = df['dias_desde_inicio'].max() + 30
        # Asumimos carga laboral constante basada en el último periodo
        empleados_actuales = df['num_empleados'].iloc[-1]
        
        prediccion = model.predict(np.array([[dias_siguiente, empleados_actuales]]))
        costo_predicho = round(prediccion[0], 2)

        return jsend_success(data={
            "prediccion_costo_siguiente_periodo": costo_predicho,
            "metodo": "Regresión Lineal Multivariable (Tiempo + Carga Laboral)",
            "metricas_validacion": {
                "r2_score": round(r2, 4),
                "interpretacion_r2": "Alta precisión" if r2 > 0.8 else "Precisión moderada",
                "error_cuadratico_medio_mse": round(mse, 2)
            },
            "variables_usadas": ["Días transcurridos", "Número de Empleados"],
            "datos_historicos_usados": len(df)
        })

    except SQLAlchemyError as e:
        return jsend_error(message=f"Error BD: {str(e)}")
    except Exception as e:
        return jsend_error(message=f"Error IA: {str(e)}")


# ==============================================================================
# 2. PATRONES DE ADELANTOS (MEJORADA CON AUTO-TUNING / SILHOUETTE)
# ==============================================================================
@router.get("/patrones-adelantos", summary="REQ-37: Clustering Inteligente con Auto-Tuning")
async def patrones_adelantos(db: Session = Depends(get_db)):
    try:
        # 1. Obtener datos
        sql_query = "SELECT amount FROM advances WHERE status = 'APPROVED' AND amount > 0;"
        df = pd.read_sql(sql_query, db.bind)

        if len(df) < 5:
            return jsend_success(data={
                "nota": "Se requieren al menos 5 adelantos aprobados para ejecutar el auto-tuning de clusters."
            })

        X = df[['amount']]
        
        # 2. Auto-Tuning: Encontrar el K óptimo usando Silhouette Score
        best_score = -1
        best_k = 3
        best_model = None
        resultados_pruebas = []

        # Probamos agrupaciones de 2, 3, 4 y 5 grupos
        rango_k = range(2, 6)
        
        for k in rango_k:
            if len(df) <= k: break
            
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X)
            
            if len(set(labels)) > 1: # Silhouette requiere al menos 2 etiquetas
                score = silhouette_score(X, labels)
            else:
                score = -1

            resultados_pruebas.append({"k_clusters": k, "calidad_score": round(score, 4)})

            if score > best_score:
                best_score = score
                best_k = k
                best_model = kmeans

        # Si algo falló y no hay modelo (ej. datos muy iguales), forzamos k=3
        if best_model is None:
            best_model = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
            best_k = 3

        # 3. Obtener resultados del mejor modelo
        centers = sorted(best_model.cluster_centers_.flatten().tolist())
        
        patrones = []
        for i, center in enumerate(centers):
            patrones.append({
                "grupo_cluster": i + 1,
                "etiqueta_sugerida": f"Nivel {i+1} (aprox. S/ {round(center)})",
                "monto_promedio": round(center, 2)
            })

        return jsend_success(data={
            "patrones_detectados": patrones,
            "metodo": "K-Means Clustering con Optimización de Silueta",
            "mejor_k_encontrado": best_k,
            "calidad_agrupamiento_score": round(best_score, 4),
            "analisis_optimizacion": resultados_pruebas
        })

    except Exception as e:
        return jsend_error(message=f"Error Clustering: {str(e)}")


# ==============================================================================
# 3. EXPORTACIÓN EXCEL (ACTUALIZADA CON LA LÓGICA NUEVA)
# ==============================================================================
@router.get("/exportar-predicciones-excel", summary="REQ-38: Exportar Reporte IA")
async def exportar_predicciones_excel(db: Session = Depends(get_db)):
    try:
        output = io.BytesIO()
        with ExcelWriter(output, engine='openpyxl') as writer:
            
            # --- Hoja 1: Predicción de Costos (Lógica Nueva) ---
            sql_costos = """
                SELECT p.start_date, COUNT(pr.id) as num_empleados, SUM(pr.net_pay) as total_cost
                FROM payrolls pr JOIN payroll_periods p ON pr.period_id = p.id
                GROUP BY p.start_date, p.id ORDER BY p.start_date;
            """
            df_costos = pd.read_sql(sql_costos, db.bind)
            
            if not df_costos.empty and len(df_costos) >= 2:
                df_hist = df_costos.copy()
                
                # Entrenamiento Rápido
                df_costos['start_date'] = pd.to_datetime(df_costos['start_date'])
                df_costos['dias'] = (df_costos['start_date'] - df_costos['start_date'].min()).dt.days
                X = df_costos[['dias', 'num_empleados']]
                y = df_costos['total_cost']
                
                model = LinearRegression().fit(X, y)
                
                # Predicción
                futuro_dias = df_costos['dias'].max() + 30
                futuro_emps = df_costos['num_empleados'].iloc[-1]
                pred = model.predict([[futuro_dias, futuro_emps]])
                r2 = r2_score(y, model.predict(X))

                # DataFrame Resultado
                df_res = pd.DataFrame([{
                    "Predicción Siguiente Periodo (S/)": round(pred[0], 2),
                    "Confianza del Modelo (R2)": round(r2, 4),
                    "Método": "Regresión Lineal Multivariable"
                }])
                
                df_res.to_excel(writer, sheet_name='Prediccion_Costos', index=False)
                df_hist.rename(columns={'total_cost': 'Costo_Planilla', 'num_empleados': 'Trabajadores'}).to_excel(writer, sheet_name='Historial_Usado', index=False)
                
                _formatear_hoja_excel(writer.sheets['Prediccion_Costos'], currency_columns=['A'])
                _formatear_hoja_excel(writer.sheets['Historial_Usado'], currency_columns=['C'])

            # --- Hoja 2: Patrones Adelantos (Lógica Nueva) ---
            sql_adv = "SELECT amount FROM advances WHERE status = 'APPROVED' AND amount > 0;"
            df_adv = pd.read_sql(sql_adv, db.bind)
            
            if len(df_adv) >= 5:
                X_adv = df_adv[['amount']]
                best_k = 3
                best_score = -1
                best_model_adv = None
                
                for k in range(2, 6):
                    if len(df_adv) <= k: break
                    km = KMeans(n_clusters=k, random_state=42, n_init=10)
                    lb = km.fit_predict(X_adv)
                    sc = silhouette_score(X_adv, lb) if len(set(lb)) > 1 else -1
                    if sc > best_score:
                        best_score = sc
                        best_k = k
                        best_model_adv = km
                
                if best_model_adv:
                    centers = sorted(best_model_adv.cluster_centers_.flatten().tolist())
                    data_patrones = [{"Grupo": f"Nivel {i+1}", "Monto Promedio (S/)": round(c, 2)} for i, c in enumerate(centers)]
                    
                    pd.DataFrame(data_patrones).to_excel(writer, sheet_name='Patrones_Adelantos', index=False)
                    _formatear_hoja_excel(writer.sheets['Patrones_Adelantos'], currency_columns=['B'])

        headers = {'Content-Disposition': 'attachment; filename="Reporte_IA_InkaPeru.xlsx"'}
        return StreamingResponse(io.BytesIO(output.getvalue()), 
                                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                                headers=headers)
    except Exception as e:
        return jsend_error(message=f"Error al generar Excel: {str(e)}")


# ==============================================================================
# 4. DETECCIÓN DE ANOMALÍAS (NUEVO: SEGURIDAD/AUDITORÍA)
# ==============================================================================
@router.get("/detectar-anomalias-asistencia", summary="REQ-EXTRA: Detección de Fraude/Anomalías con Isolation Forest")
async def detectar_anomalias_asistencia(db: Session = Depends(get_db)):
    try:
        # 1. Obtener datos de asistencia (Hora de entrada y Horas trabajadas)
        #    Convertimos la hora de entrada a minutos del día (ej. 8:00 AM = 480 min)
        sql_query = """
            SELECT 
                e.nombre,
                ar.record_date,
                TIME_TO_SEC(ar.time_in) / 60 as ingreso_minutos,
                ar.work_hours
            FROM attendance_records ar
            JOIN employees e ON ar.employee_id = e.id
            WHERE ar.time_in IS NOT NULL AND ar.work_hours IS NOT NULL;
        """
        df = pd.read_sql(sql_query, db.bind)

        if len(df) < 10:
            return jsend_success(data={
                "nota": "Se necesitan al menos 10 registros para detectar anomalías confiables."
            })

        # 2. Preparamos los datos para la IA
        #    La IA buscará relaciones extrañas entre A qué hora entras vs Cuánto trabajas
        X = df[['ingreso_minutos', 'work_hours']]

        # 3. Entrenamos Isolation Forest
        #    contamination=0.05 significa que asume que aprox el 5% de datos son "raros"
        model = IsolationForest(contamination=0.05, random_state=42)
        df['anomaly_score'] = model.fit_predict(X) # -1 es anomalía, 1 es normal

        # 4. Filtramos solo los casos raros (-1)
        anomalias = df[df['anomaly_score'] == -1].copy()
        
        # Formateamos para enviar al frontend
        resultado = []
        for _, row in anomalias.iterrows():
            hora_legible = f"{int(row['ingreso_minutos'] // 60):02d}:{int(row['ingreso_minutos'] % 60):02d}"
            resultado.append({
                "empleado": row['nombre'],
                "fecha": str(row['record_date']),
                "hora_ingreso": hora_legible,
                "horas_trabajadas": row['work_hours'],
                "motivo_ia": "Comportamiento inusual detectado (Outlier estadístico)"
            })

        return jsend_success(data={
            "total_registros_analizados": len(df),
            "anomalias_detectadas": len(resultado),
            "registros_sospechosos": resultado,
            "metodo": "Isolation Forest (Detección de Outliers)",
            "explicacion": "La IA ha detectado registros que se desvían matemáticamente del patrón normal de la empresa."
        })

    except Exception as e:
        return jsend_error(message=f"Error Anomalías: {str(e)}")