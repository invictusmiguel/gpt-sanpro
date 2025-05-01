# 🚀 scripts/etl_auto_update.py
import sqlite3
import pandas as pd
from datetime import datetime
import os

# 📦 Simulación de lectura del ETL sabermétrico
def run_etl():
    # 🧪 Aquí deberías importar datos desde CSV, web o lo que sea
    # Este ejemplo simula 3 partidos
    data = {
        "equipo_local": ["Yankees", "Dodgers", "Mets"],
        "equipo_visitante": ["Red Sox", "Giants", "Phillies"],
        "obp_local": [0.320, 0.310, 0.300],
        "slg_local": [0.450, 0.460, 0.440],
        "era_pitcher_local": [3.20, 3.50, 3.00],
        "obp_visitante": [0.300, 0.295, 0.310],
        "slg_visitante": [0.410, 0.430, 0.420],
        "era_pitcher_visitante": [3.10, 3.60, 2.90],
        "fecha": [datetime.now().date()] * 3
    }
    df = pd.DataFrame(data)
    return df

# 🧠 Inserta los datos en SQLite
def insertar_en_base(df, db_path='partidos.db'):
    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql('partidos', conn, if_exists='append', index=False)
        return True, len(df)
    except Exception as e:
        return False, str(e)

# 📓 Guarda log en logs/etl_log.csv
def guardar_log(partidos_insertados, estado):
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    log_path = "logs/etl_log.csv"

    os.makedirs("logs", exist_ok=True)
    log_data = pd.DataFrame([{
        "fecha": fecha,
        "hora": hora,
        "partidos_insertados": partidos_insertados,
        "estado": estado
    }])

    if os.path.exists(log_path):
        log_data.to_csv(log_path, mode='a', index=False, header=False)
    else:
        log_data.to_csv(log_path, index=False)

# 🧪 Ejecutar todo el flujo
if __name__ == "__main__":
    print("🚀 Ejecutando ETL automático...")
    df_partidos = run_etl()

    if df_partidos.empty:
        print("⚠️ No se encontraron partidos nuevos.")
        guardar_log(0, "sin_datos")
    else:
        ok, resultado = insertar_en_base(df_partidos)
        if ok:
            print(f"✅ Insertados {resultado} partidos.")
            guardar_log(resultado, "exito")
        else:
            print(f"❌ Error al insertar: {resultado}")
            guardar_log(0, f"error: {resultado}")
