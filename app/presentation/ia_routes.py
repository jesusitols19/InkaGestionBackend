import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import numpy as np

from app.dependencies import get_db
from app.helpers.jsend_response import jsend_success, jsend_error

router = APIRouter()

# --- REQ-36: Estimar costos de planillas futuros ---
# --- REQ-35: Predecir costo total de una jornada futura ---
# (Usaremos la misma técnica para ambos por VELOCIDAD: Regresión Lineal)

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