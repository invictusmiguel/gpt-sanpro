# train_model.py

# 📚 Importaciones
import pandas as pd
import sqlite3
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import joblib

# 📚 Leer datos desde SQLite
def load_data(database_path="database/partidos.db"):
    print("🔹 Cargando datos desde la base de datos...")
    conn = sqlite3.connect(database_path)
    df = pd.read_sql_query("SELECT * FROM partidos", conn)
    conn.close()
    print(f"✅ {df.shape[0]} registros cargados.")
    return df

# 🧹 Limpieza inicial
def clean_data(df):
    print("🔹 Limpiando datos...")

    # Eliminar registros con valores nulos en columnas numéricas
    num_cols = [
        'obp_local', 'slg_local', 'woba_local',
        'obp_visitante', 'slg_visitante', 'woba_visitante',
        'era_pitcher_local', 'fip_pitcher_local',
        'era_pitcher_visitante', 'fip_pitcher_visitante',
        'resultado_local', 'resultado_visitante'
    ]
    df = df.dropna(subset=num_cols)

    # Eliminar partidos empatados
    df = df[df['resultado_local'] != df['resultado_visitante']]

    print(f"✅ {df.shape[0]} registros después de limpieza.")
    return df

# 🏗️ Creación de variables derivadas
def feature_engineering(df):
    print("🔹 Generando variables derivadas...")

    # Diferencia de carreras
    df['diferencial_carreras'] = df['resultado_local'] - df['resultado_visitante']

    # Equipo ganador: 1 = local ganó, 0 = visitante ganó
    df['equipo_ganador'] = df.apply(lambda row: 1 if row['resultado_local'] > row['resultado_visitante'] else 0, axis=1)

    # Diferencias estadísticas
    df['obp_diff'] = df['obp_local'] - df['obp_visitante']
    df['slg_diff'] = df['slg_local'] - df['slg_visitante']
    df['woba_diff'] = df['woba_local'] - df['woba_visitante']
    df['era_diff'] = df['era_pitcher_visitante'] - df['era_pitcher_local']
    df['fip_diff'] = df['fip_pitcher_visitante'] - df['fip_pitcher_local']

    print("✅ Variables derivadas generadas.")
    return df

# 🧠 Preparar datasets
def prepare_datasets(csv_path="data/partidos_preprocesados.csv"):
    print("🔹 Preparando datasets para entrenamiento...")

    # Leer el CSV procesado
    df = pd.read_csv(csv_path)

    # Definir features y targets
    features = ['obp_diff', 'slg_diff', 'woba_diff', 'era_diff', 'fip_diff']
    X = df[features]
    y_regresion = df['diferencial_carreras']
    y_clasificacion = df['equipo_ganador']

    # Escalar features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # División en entrenamiento y prueba (80%/20%)
    X_train, X_test, y_train_reg, y_test_reg = train_test_split(X_scaled, y_regresion, test_size=0.2, random_state=42)
    _, _, y_train_clf, y_test_clf = train_test_split(X_scaled, y_clasificacion, test_size=0.2, random_state=42)

    print("✅ Datos escalados y divididos correctamente.")
    return X_train, X_test, y_train_reg, y_test_reg, y_train_clf, y_test_clf, scaler
# 🏋️‍♂️ Entrenar y guardar los modelos
def train_and_save_models(X_train, X_test, y_train_reg, y_test_reg, y_train_clf, y_test_clf, scaler):
    print("🔹 Entrenando modelos...")

    # 🔥 Modelo de Regresión (para predecir diferencial de carreras)
    modelo_regresion = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42)
    modelo_regresion.fit(X_train, y_train_reg)

    # 🔥 Modelo de Clasificación (para predecir equipo ganador)
    modelo_clasificacion = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    modelo_clasificacion.fit(X_train, y_train_clf)

    # 📦 Crear carpeta /models si no existe
    if not os.path.exists('models'):
        os.makedirs('models')

    # 💾 Guardar los modelos entrenados
    joblib.dump(modelo_regresion, 'models/modelo_regresion.pkl')
    joblib.dump(modelo_clasificacion, 'models/modelo_clasificacion.pkl')
    joblib.dump(scaler, 'models/escalador.pkl')

    print("✅ Modelos entrenados y guardados en /models/")
    return modelo_regresion, modelo_clasificacion

# 🚀 Función principal
def main():
    df = load_data()
    df = clean_data(df)
    df = feature_engineering(df)

    # Guardar dataset preprocesado
    if not os.path.exists('data'):
        os.makedirs('data')
    df.to_csv('data/partidos_preprocesados.csv', index=False)
    print("✅ Datos preprocesados guardados en data/partidos_preprocesados.csv")

    # Preparar datasets para entrenamiento
    X_train, X_test, y_train_reg, y_test_reg, y_train_clf, y_test_clf, scaler = prepare_datasets()

    # Entrenar y guardar modelos
    train_and_save_models(X_train, X_test, y_train_reg, y_test_reg, y_train_clf, y_test_clf, scaler)

# 🧠 Ejecutar main
if __name__ == "__main__":
    main()
