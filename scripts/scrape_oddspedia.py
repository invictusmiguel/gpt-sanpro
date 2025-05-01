# 🚀 scripts/scrape_oddspedia.py
import os
import json
import pandas as pd
from datetime import datetime

# 📦 Simulación de scraper de cuotas deportivas
def extraer_cuotas():
    partidos = []
    for i in range(12):  # Simulamos 12 partidos
        partido = {
            "evento": f"Equipo {i+1} vs Equipo {i+2}",
            "cuota": round(1.80 + 0.05 * i, 2),
            "probabilidad": round(0.50 + 0.01 * i, 2),
            "mercado": "ML",
            "fecha": datetime.now().strftime("%Y-%m-%d")
        }
        partidos.append(partido)
    return partidos

# 📥 Guardar archivo JSON
def guardar_json(data, path="data/cuotas_mlbbulk.json"):
    os.makedirs("data", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# 📝 Registrar log
def guardar_log(partidos_extraidos, estado):
    os.makedirs("logs", exist_ok=True)
    log_path = "logs/cuotas_log.csv"
    now = datetime.now()
    log_entry = pd.DataFrame([{
        "fecha": now.strftime("%Y-%m-%d"),
        "hora": now.strftime("%H:%M:%S"),
        "partidos_extraidos": partidos_extraidos,
        "estado": estado
    }])

    if os.path.exists(log_path):
        log_entry.to_csv(log_path, mode='a', index=False, header=False)
    else:
        log_entry.to_csv(log_path, index=False)

# 🚀 Ejecutar proceso completo
if __name__ == "__main__":
    print("🎯 Ejecutando scrape_oddspedia.py...")
    cuotas = extraer_cuotas()

    if len(cuotas) < 10:
        print("⚠️ No se extrajeron suficientes partidos. Mínimo requerido: 10.")
        guardar_log(len(cuotas), "insuficiente")
    else:
        guardar_json(cuotas)
        print(f"✅ Cuotas guardadas: {len(cuotas)} partidos.")
        guardar_log(len(cuotas), "exito")
