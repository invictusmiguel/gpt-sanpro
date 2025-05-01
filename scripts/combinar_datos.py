# 🚀 scripts/combinar_datos.py
import os
import json
import random
import pandas as pd
from datetime import datetime

CUOTAS_PATH = "data/cuotas_mlbbulk.json"
OUTPUT_PATH = "data/cuotas_diarias.json"
LOG_PATH = "logs/integracion_log.csv"

# 📥 Leer cuotas desde archivo JSON
def leer_cuotas():
    if not os.path.exists(CUOTAS_PATH):
        raise FileNotFoundError("No se encontró cuotas_mlbbulk.json")
    with open(CUOTAS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# 🧠 Simular probabilidades, clima y confianza
def enriquecer_pick(pick):
    probabilidad = round(random.uniform(0.60, 0.80), 2)
    valor_esperado = round(probabilidad * pick["cuota"], 2)

    return {
        "evento": pick["evento"],
        "cuota": pick["cuota"],
        "probabilidad": probabilidad,
        "valor_esperado": valor_esperado,
        "confianza": "Alta" if probabilidad >= 0.70 else "Media",
        "pitcher_ok": random.choice([True, False]),
        "clima": random.choice(["Soleado", "Nublado", "Lluvia"])
    }

# 📝 Guardar archivo final
def guardar_json(data):
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump({"partidos": data}, f, indent=4, ensure_ascii=False)

# 🧾 Guardar log de integración
def guardar_log(cantidad, estado):
    now = datetime.now()
    os.makedirs("logs", exist_ok=True)
    log_entry = pd.DataFrame([{
        "fecha": now.strftime("%Y-%m-%d"),
        "hora": now.strftime("%H:%M:%S"),
        "items_generados": cantidad,
        "estado": estado
    }])

    if os.path.exists(LOG_PATH):
        log_entry.to_csv(LOG_PATH, mode='a', header=False, index=False)
    else:
        log_entry.to_csv(LOG_PATH, index=False)

# 🚀 Ejecutar
if __name__ == "__main__":
    print("🔗 Combinando datos...")
    try:
        cuotas = leer_cuotas()

        if len(cuotas) < 10:
            print("⚠️ Menos de 10 cuotas disponibles.")
            guardar_log(len(cuotas), "insuficiente")
        else:
            combinados = [enriquecer_pick(p) for p in cuotas]
            guardar_json(combinados)
            print(f"✅ Generado cuotas_diarias.json con {len(combinados)} picks.")
            guardar_log(len(combinados), "ok")
    except Exception as e:
        print(f"❌ Error en combinar_datos: {e}")
        guardar_log(0, f"error: {str(e)}")
# 🚀 scripts/combinar_datos.py
import os
import json
import random
import pandas as pd
from datetime import datetime

CUOTAS_PATH = "data/cuotas_mlbbulk.json"
OUTPUT_PATH = "data/cuotas_diarias.json"
LOG_PATH = "logs/integracion_log.csv"

# 📥 Leer cuotas desde archivo JSON
def leer_cuotas():
    if not os.path.exists(CUOTAS_PATH):
        raise FileNotFoundError("No se encontró cuotas_mlbbulk.json")
    with open(CUOTAS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# 🧠 Simular probabilidades, clima y confianza
def enriquecer_pick(pick):
    probabilidad = round(random.uniform(0.60, 0.80), 2)
    valor_esperado = round(probabilidad * pick["cuota"], 2)

    return {
        "evento": pick["evento"],
        "cuota": pick["cuota"],
        "probabilidad": probabilidad,
        "valor_esperado": valor_esperado,
        "confianza": "Alta" if probabilidad >= 0.70 else "Media",
        "pitcher_ok": random.choice([True, False]),
        "clima": random.choice(["Soleado", "Nublado", "Lluvia"])
    }

# 📝 Guardar archivo final
def guardar_json(data):
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump({"partidos": data}, f, indent=4, ensure_ascii=False)

# 🧾 Guardar log de integración
def guardar_log(cantidad, estado):
    now = datetime.now()
    os.makedirs("logs", exist_ok=True)
    log_entry = pd.DataFrame([{
        "fecha": now.strftime("%Y-%m-%d"),
        "hora": now.strftime("%H:%M:%S"),
        "items_generados": cantidad,
        "estado": estado
    }])

    if os.path.exists(LOG_PATH):
        log_entry.to_csv(LOG_PATH, mode='a', header=False, index=False)
    else:
        log_entry.to_csv(LOG_PATH, index=False)

# 🚀 Ejecutar
if __name__ == "__main__":
    print("🔗 Combinando datos...")
    try:
        cuotas = leer_cuotas()

        if len(cuotas) < 10:
            print("⚠️ Menos de 10 cuotas disponibles.")
            guardar_log(len(cuotas), "insuficiente")
        else:
            combinados = [enriquecer_pick(p) for p in cuotas]
            guardar_json(combinados)
            print(f"✅ Generado cuotas_diarias.json con {len(combinados)} picks.")
            guardar_log(len(combinados), "ok")
    except Exception as e:
        print(f"❌ Error en combinar_datos: {e}")
        guardar_log(0, f"error: {str(e)}")
