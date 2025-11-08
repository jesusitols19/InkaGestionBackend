import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import numpy as np
from pandas import ExcelWriter
from openpyxl.styles import Font, Alignment
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import get_column_letter

import io
from fastapi.responses import StreamingResponse
from app.dependencies import get_db
from app.helpers.jsend_response import jsend_success, jsend_error

router = APIRouter()


def _formatear_hoja_excel(worksheet: Worksheet, currency_columns: list = []):
    """
    Aplica estilos profesionales a una hoja de cálculo de openpyxl.
    - Autoajusta el ancho de las columnas.
    - Pone el encabezado en negrita.
    - Aplica formato de moneda a las columnas especificadas.
    """
    header_font = Font(bold=True)
    
    # Iteramos sobre todas las celdas para autoajustar y aplicar estilos
    for r_idx, row in enumerate(worksheet.iter_rows(), 1):
        for c_idx, cell in enumerate(row, 1):
            col_letter = get_column_letter(c_idx)
            
            # Poner encabezado (fila 1) en negrita
            if r_idx == 1:
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center")

            # Ajustar ancho de columna (simple aproximación)
            current_width = worksheet.column_dimensions[col_letter].width
            new_width = len(str(cell.value)) * 1.2
            if new_width > (current_width or 10):
                worksheet.column_dimensions[col_letter].width = min(new_width, 50) # Max 50
            
            # Aplicar formato de moneda
            if r_idx > 1 and col_letter in currency_columns:
                cell.number_format = '"S/ "#,##0.00' # Formato: S/ 1,234.56

@router.get("/predecir-costos-planilla", summary="REQ-35 y REQ-36: Predice costos futuros de planilla")
async def predecir_costos_planilla(db: Session = Depends(get_db)):
    """
    Usa Regresión Lineal para predecir el costo total de la siguiente planilla
    basándose en los costos de las planillas pasadas.
    """
    try:
        # 1. Consulta SQL para obtener los datos históricos de costos de planilla
        #    Agrupamos por periodo para tener el costo total de cada planilla.
        sql_query = """
            SELECT 
                p.start_date, 
                SUM(pr.net_pay) as total_cost
            FROM payrolls pr
            JOIN payroll_periods p ON pr.period_id = p.id
            GROUP BY p.start_date, p.id
            ORDER BY p.start_date;
        """
        
        # 2. Cargar datos en un DataFrame de Pandas
        df = pd.read_sql(sql_query, db.bind)

        if df.empty or len(df) < 2:
            return jsend_success(data={
                "prediccion_costo_siguiente_periodo": 0,
                "nota": "No hay suficientes datos históricos (necesita al menos 2 periodos de planilla) para predecir."
            })

        # 3. Preparar datos para scikit-learn
        df['start_date'] = pd.to_datetime(df['start_date'])
        # Creamos una variable numérica para el tiempo (días desde el inicio)
        df['dias_desde_inicio'] = (df['start_date'] - df['start_date'].min()).dt.days
        
        X = df[['dias_desde_inicio']]  # Datos de entrada (tiempo)
        y = df['total_cost']         # Datos de salida (costo)

        # 4. "Entrenar" el modelo de Regresión Lineal
        model = LinearRegression()
        model.fit(X, y)

        # 5. "Predecir"
        #    Vamos a predecir el siguiente periodo. Asumimos que los periodos son
        #    regulares (ej. 30 días).
        dias_siguiente_prediccion = df['dias_desde_inicio'].max() + 30 # Asumiendo periodos de 30 días
        
        prediccion = model.predict(np.array([[dias_siguiente_prediccion]]))
        costo_predicho = round(prediccion[0], 2)

        return jsend_success(data={
            "prediccion_costo_siguiente_periodo": costo_predicho,
            "metodo": "Regresión Lineal Simple",
            "datos_historicos_usados": df.to_dict('records')
        })

    except SQLAlchemyError as e:
        return jsend_error(message=f"Error de base de datos: {str(e)}")
    except Exception as e:
        return jsend_error(message=f"Error inesperado: {str(e)}")


# --- REQ-37: Identificar patrones en solicitudes de adelantos ---

@router.get("/patrones-adelantos", summary="REQ-37: Identifica patrones en solicitudes de adelantos")
async def patrones_adelantos(db: Session = Depends(get_db)):
    """
    Usa Clustering (K-Means) para agrupar las solicitudes de adelanto
    aprobadas por monto, identificando patrones de "pequeño", "mediano" y "grande".
    """
    try:
        # 1. Consulta SQL: Traer todos los montos de adelantos aprobados
        #    Tu tabla 'advances' NO tiene 'motivo', así que agruparemos por 'amount'.
        sql_query = """
            SELECT amount FROM advances 
            WHERE status = 'APPROVED' AND amount > 0;
        """

        # 2. Cargar datos en DataFrame
        df = pd.read_sql(sql_query, db.bind)

        # KMeans necesita al menos 3 muestras para 3 clusters
        if df.empty or len(df) < 3:
            return jsend_success(data={
                "patrones_clusters": [],
                "nota": "No hay suficientes adelantos aprobados (necesita al menos 3) para clustering."
            })

        # 3. "Entrenar" el modelo de Clustering (K-Means)
        #    Vamos a buscar 3 clusters (pequeño, mediano, grande)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        kmeans.fit(df[['amount']])

        # 4. Obtener los centros de los clusters (los montos promedio de cada grupo)
        centers = sorted(kmeans.cluster_centers_.flatten().tolist())
        
        patrones = [
            {"cluster": "Patrón 'Adelanto Pequeño'", "monto_promedio": round(centers[0], 2)},
            {"cluster": "Patrón 'Adelanto Mediano'", "monto_promedio": round(centers[1], 2)},
            {"cluster": "Patrón 'Adelanto Grande'", "monto_promedio": round(centers[2], 2)}
        ]

        return jsend_success(data={
            "patrones_clusters": patrones,
            "metodo": "Clustering K-Means"
        })

    except SQLAlchemyError as e:
        return jsend_error(message=f"Error de base de datos: {str(e)}")
    except Exception as e:
        return jsend_error(message=f"Error inesperado: {str(e)}")
    
    
@router.get("/exportar-predicciones-excel", summary="REQ-38: Exporta todas las predicciones a Excel")
async def exportar_predicciones_excel(db: Session = Depends(get_db)):
    try:
        output = io.BytesIO()
        with ExcelWriter(output, engine='openpyxl') as writer:
            
            # --- Lógica 1: Predicción de Costos ---
            sql_costos = """
                SELECT p.start_date, SUM(pr.net_pay) as total_cost
                FROM payrolls pr JOIN payroll_periods p ON pr.period_id = p.id
                GROUP BY p.start_date, p.id ORDER BY p.start_date;
            """
            df_costos = pd.read_sql(sql_costos, db.bind)
            
            if not df_costos.empty and len(df_costos) >= 2:
                df_costos_historicos = df_costos.copy() # Guardamos los datos puros
                
                df_costos['start_date'] = pd.to_datetime(df_costos['start_date'])
                df_costos['dias_desde_inicio'] = (df_costos['start_date'] - df_costos['start_date'].min()).dt.days
                X = df_costos[['dias_desde_inicio']]
                y = df_costos['total_cost']
                model = LinearRegression()
                model.fit(X, y)
                dias_siguiente = df_costos['dias_desde_inicio'].iloc[-1] + 30
                prediccion = model.predict(np.array([[dias_siguiente]]))
                costo_predicho = round(prediccion[0], 2)
                
                df_prediccion = pd.DataFrame({
                    "Concepto": ["Predicción Próximo Periodo"],
                    "Valor Estimado (S/)": [costo_predicho],
                    "Metodo": ["Regresión Lineal"]
                })
                
                # Escribimos a las Hojas y aplicamos formato
                df_prediccion.to_excel(writer, sheet_name='Prediccion_Costos', index=False)
                _formatear_hoja_excel(writer.sheets['Prediccion_Costos'], currency_columns=['B'])
                
                # Renombramos columnas para el historial
                df_costos_historicos.rename(columns={'start_date': 'Inicio_Periodo', 'total_cost': 'Costo_Total_Soles'}, inplace=True)
                df_costos_historicos.to_excel(writer, sheet_name='Historial_Costos', index=False)
                _formatear_hoja_excel(writer.sheets['Historial_Costos'], currency_columns=['B'])

            # --- Lógica 2: Patrones de Adelantos ---
            sql_adelantos = "SELECT amount FROM advances WHERE status = 'APPROVED' AND amount > 0;"
            df_adelantos = pd.read_sql(sql_adelantos, db.bind)

            if not df_adelantos.empty and len(df_adelantos) >= 3:
                kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
                kmeans.fit(df_adelantos[['amount']])
                centers = sorted(kmeans.cluster_centers_.flatten().tolist())
                
                df_patrones = pd.DataFrame([
                    {"Patron_Detectado": "Adelanto Pequeño", "Monto_Promedio_Soles": round(centers[0], 2)},
                    {"Patron_Detectado": "Adelanto Mediano", "Monto_Promedio_Soles": round(centers[1], 2)},
                    {"Patron_Detectado": "Adelanto Grande", "Monto_Promedio_Soles": round(centers[2], 2)}
                ])
                df_patrones.to_excel(writer, sheet_name='Patrones_Adelantos', index=False)
                _formatear_hoja_excel(writer.sheets['Patrones_Adelantos'], currency_columns=['B'])

        headers = {'Content-Disposition': 'attachment; filename="Reporte_Predicciones_IA.xlsx"'}
        return StreamingResponse(io.BytesIO(output.getvalue()), 
                                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                                headers=headers)
    except Exception as e:
        return jsend_error.error(message=f"Error al generar Excel: {str(e)}")