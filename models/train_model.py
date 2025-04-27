# models/train_model.py

# 📦 Importaciones necesarias
import pandas as pd
import sqlite3

# 📈 Fase 1: Cargar datos desde SQLite
def cargar_datos():
    print("🔵 Cargando datos desde la base de datos partidos.db...")

    try:
        conn = sqlite3.connect('database/partidos.db')
        query = "SELECT * FROM partidos"
        df = pd.read_sql_query(query, conn)
        conn.close()
    except Exception as e:
        print(f"❌ Error al cargar los datos: {e}")
        return pd.DataFrame()

    print(f"✅ {len(df)} registros cargados exitosamente.")
    return df

# 🚀 Ejecutar carga solo si corres este script directamente
if __name__ == "__main__":
    df = cargar_datos()
    print(df.head())
# 📈 Fase 2: Crear features (X) y targets (y)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def preparar_datos(df):
    print("🟠 Preparando features y targets para los modelos...")

    # Eliminamos filas incompletas
    df = df.dropna(subset=[
        'obp_local', 'slg_local', 'woba_local',
        'obp_visitante', 'slg_visitante', 'woba_visitante',
        'era_pitcher_local', 'fip_pitcher_local',
        'era_pitcher_visitante', 'fip_pitcher_visitante',
        'resultado_local', 'resultado_visitante'
    ])

    # Features para ambos modelos
    features = [
        'obp_local', 'slg_local', 'woba_local',
        'obp_visitante', 'slg_visitante', 'woba_visitante',
        'era_pitcher_local', 'fip_pitcher_local',
        'era_pitcher_visitante', 'fip_pitcher_visitante'
    ]
    
    X = df[features]

    # Target para regresión: diferencial de carreras
    y_reg = df['resultado_local'] - df['resultado_visitante']

    # Target para clasificación: quién gana (local=1, visitante=0)
    y_clf = (df['resultado_local'] > df['resultado_visitante']).astype(int)

    # Escalar las features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("✅ Features y targets preparados.")
    return X_scaled, y_reg, y_clf, scaler
# 📈 Fase 3: Entrenar modelo de regresión

from sklearn.ensemble import RandomForestRegressor

def entrenar_modelo_regresion(X, y_reg):
    print("🟠 Entrenando modelo de regresión (diferencial de carreras)...")

    modelo_regresion = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    modelo_regresion.fit(X, y_reg)

    print("✅ Modelo de regresión entrenado.")
    return modelo_regresion
# 📈 Fase 4: Entrenar modelo de clasificación

from sklearn.ensemble import RandomForestClassifier

def entrenar_modelo_clasificacion(X, y_clf):
    print("🟠 Entrenando modelo de clasificación (ganador local o visitante)...")

    modelo_clasificacion = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    modelo_clasificacion.fit(X, y_clf)

    print("✅ Modelo de clasificación entrenado.")
    return modelo_clasificacion
# 💾 Fase 5: Guardar modelos y scaler

import joblib
import os

def guardar_modelos(modelo_regresion, modelo_clasificacion, scaler):
    print("🟢 Guardando modelos entrenados y scaler...")

    # Crear carpeta models si no existe
    os.makedirs('models', exist_ok=True)

    # Guardar modelos y scaler
    joblib.dump(modelo_regresion, 'models/regression_model.pkl')
    joblib.dump(modelo_clasificacion, 'models/classification_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')

    print("✅ Modelos y scaler guardados exitosamente en carpeta models/")
# 🏗️ Fase 6: Función principal para ejecutar todo el entrenamiento

def main():
    print("🚀 Iniciando entrenamiento de modelos SAMPRO...")

    # 1. Cargar datos
    df = cargar_datos()

    # 2. Preparar datos
    X_scaled, y_reg, y_clf, scaler = preparar_datos(df)

    # 3. Entrenar modelo de regresión
    modelo_regresion = entrenar_modelo_regresion(X_scaled, y_reg)

    # 4. Entrenar modelo de clasificación
    modelo_clasificacion = entrenar_modelo_clasificacion(X_scaled, y_clf)

    # 5. Guardar todo
    guardar_modelos(modelo_regresion, modelo_clasificacion, scaler)

    print("🏆 Entrenamiento y guardado de modelos completado exitosamente.")

# 🚀 Ejecutar el script
if __name__ == "__main__":
    main()
