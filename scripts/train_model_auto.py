# 🚀 scripts/train_model_auto.py
import os
import sqlite3
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

DB_PATH = "partidos.db"
LOG_PATH = "logs/retrain_log.csv"
MODEL_DIR = "models"

# 🧠 Cargar datos desde base SQLite
def cargar_datos():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql("SELECT * FROM partidos", conn)
    return df

# 🧪 Entrenamiento de modelos
def entrenar_modelos(df):
    os.makedirs(MODEL_DIR, exist_ok=True)

    df["target_diff"] = df["slg_local"] - df["slg_visitante"]  # Simulación
    df["target_win_local"] = (df["target_diff"] > 0).astype(int)

    X = df[[
        "obp_local", "slg_local", "woba_local", "era_pitcher_local", "fip_pitcher_local",
        "obp_visitante", "slg_visitante", "woba_visitante", "era_pitcher_visitante", "fip_pitcher_visitante"
    ]]
    y_reg = df["target_diff"]
    y_clf = df["target_win_local"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model_reg = LinearRegression()
    model_reg.fit(X_scaled, y_reg)

    model_clf = LogisticRegression()
    model_clf.fit(X_scaled, y_clf)

    # Guardar modelos
    joblib.dump(model_reg, f"{MODEL_DIR}/regression_model.pkl")
    joblib.dump(model_clf, f"{MODEL_DIR}/classification_model.pkl")
    joblib.dump(scaler, f"{MODEL_DIR}/scaler.pkl")

    return len(df)

# 📓 Guardar log
def guardar_log(cantidad, estado):
    now = datetime.now()
    os.makedirs("logs", exist_ok=True)

    log_entry = pd.DataFrame([{
        "fecha": now.strftime("%Y-%m-%d"),
        "hora": now.strftime("%H:%M:%S"),
        "modelo": "reg+clf",
        "partidos_usados": cantidad,
        "estado": estado
    }])

    if os.path.exists(LOG_PATH):
        log_entry.to_csv(LOG_PATH, mode="a", header=False, index=False)
    else:
        log_entry.to_csv(LOG_PATH, index=False)

# 🚀 Ejecutar
if __name__ == "__main__":
    print("🔍 Buscando nuevos datos para reentrenar...")
    try:
        df = cargar_datos()
        cantidad = len(df)

        if cantidad < 10:
            print(f"⚠️ Solo hay {cantidad} partidos. No se entrena.")
            guardar_log(cantidad, "insuficiente")
        else:
            usados = entrenar_modelos(df)
            print(f"✅ Modelos entrenados con {usados} partidos.")
            guardar_log(usados, "entrenado")
    except Exception as e:
        print(f"❌ Error: {e}")
        guardar_log(0, f"error: {str(e)}")
