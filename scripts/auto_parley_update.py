# 🚀 scripts/auto_parley_update.py
import os
import json
import pandas as pd
from datetime import datetime
import random

CUOTAS_PATH = "data/cuotas_diarias.json"
PARLEY_PATH = "data/parleys_generados.json"
LOG_PATH = "logs/parley_log.csv"

# ✅ Leer los picks desde cuotas_diarias.json
def leer_cuotas():
    with open(CUOTAS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("partidos", [])

# 🧠 Generar parley cumpliendo reglas matemáticas
def generar_parley(picks):
    # Mezclamos para variedad
    random.shuffle(picks)

    parley = []
    cuota_total = 1
    prob_total = 1
    ve_total = 0

    for pick in picks:
        cuota = pick.get("cuota", 1)
        prob = pick.get("probabilidad", 0.5)
        ve = pick.get("valor_esperado", cuota * prob)

        cuota_total *= cuota
        prob_total *= prob
        ve_total += ve

        parley.append(pick)

        # Cortamos cuando cumple condiciones mínimas
        if cuota_total >= 3.5 and prob_total >= 0.30 and ve_total >= 1.0:
            break

    if cuota_total >= 3.5 and prob_total >= 0.30 and ve_total >= 1.0:
        return {
            "picks": parley,
            "cuota_total": round(cuota_total, 2),
            "probabilidad_total": round(prob_total, 2),
            "valor_esperado_total": round(ve_total, 2)
        }
    else:
        return None

# 💾 Guardar parley en JSON
def guardar_parley(parley):
    os.makedirs("data", exist_ok=True)
    with open(PARLEY_PATH, "w", encoding="utf-8") as f:
        json.dump(parley, f, indent=4, ensure_ascii=False)

# 📝 Registrar log
def guardar_log(picks_total, estado):
    os.makedirs("logs", exist_ok=True)
    now = datetime.now()
    log_entry = pd.DataFrame([{
        "fecha": now.strftime("%Y-%m-%d"),
        "hora": now.strftime("%H:%M:%S"),
        "picks_enviados": picks_total,
        "estado": estado
    }])
    if os.path.exists(LOG_PATH):
        log_entry.to_csv(LOG_PATH, mode="a", header=False, index=False)
    else:
        log_entry.to_csv(LOG_PATH, index=False)

# 🚀 Ejecutar
if __name__ == "__main__":
    print("🎯 Generando Parley del Día...")
    try:
        picks = leer_cuotas()
        if len(picks) < 5:
            print("⚠️ No hay suficientes picks para generar parley.")
            guardar_log(len(picks), "insuficiente")
        else:
            resultado = generar_parley(picks)
            if resultado:
                guardar_parley(resultado)
                print(f"✅ Parley generado: {len(resultado['picks'])} picks.")
                guardar_log(len(resultado["picks"]), "generado")
            else:
                print("❌ No se pudo generar un parley que cumpla las reglas.")
                guardar_log(len(picks), "no_apto")
    except Exception as e:
        print(f"❌ Error al generar parley: {e}")
        guardar_log(0, f"error: {str(e)}")
# 🚀 scripts/auto_parley_update.py
import os
import json
import pandas as pd
from datetime import datetime
import random

CUOTAS_PATH = "data/cuotas_diarias.json"
PARLEY_PATH = "data/parleys_generados.json"
LOG_PATH = "logs/parley_log.csv"

# ✅ Leer los picks desde cuotas_diarias.json
def leer_cuotas():
    with open(CUOTAS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("partidos", [])

# 🧠 Generar parley cumpliendo reglas matemáticas
def generar_parley(picks):
    # Mezclamos para variedad
    random.shuffle(picks)

    parley = []
    cuota_total = 1
    prob_total = 1
    ve_total = 0

    for pick in picks:
        cuota = pick.get("cuota", 1)
        prob = pick.get("probabilidad", 0.5)
        ve = pick.get("valor_esperado", cuota * prob)

        cuota_total *= cuota
        prob_total *= prob
        ve_total += ve

        parley.append(pick)

        # Cortamos cuando cumple condiciones mínimas
        if cuota_total >= 3.5 and prob_total >= 0.30 and ve_total >= 1.0:
            break

    if cuota_total >= 3.5 and prob_total >= 0.30 and ve_total >= 1.0:
        return {
            "picks": parley,
            "cuota_total": round(cuota_total, 2),
            "probabilidad_total": round(prob_total, 2),
            "valor_esperado_total": round(ve_total, 2)
        }
    else:
        return None

# 💾 Guardar parley en JSON
def guardar_parley(parley):
    os.makedirs("data", exist_ok=True)
    with open(PARLEY_PATH, "w", encoding="utf-8") as f:
        json.dump(parley, f, indent=4, ensure_ascii=False)

# 📝 Registrar log
def guardar_log(picks_total, estado):
    os.makedirs("logs", exist_ok=True)
    now = datetime.now()
    log_entry = pd.DataFrame([{
        "fecha": now.strftime("%Y-%m-%d"),
        "hora": now.strftime("%H:%M:%S"),
        "picks_enviados": picks_total,
        "estado": estado
    }])
    if os.path.exists(LOG_PATH):
        log_entry.to_csv(LOG_PATH, mode="a", header=False, index=False)
    else:
        log_entry.to_csv(LOG_PATH, index=False)

# 🚀 Ejecutar
if __name__ == "__main__":
    print("🎯 Generando Parley del Día...")
    try:
        picks = leer_cuotas()
        if len(picks) < 5:
            print("⚠️ No hay suficientes picks para generar parley.")
            guardar_log(len(picks), "insuficiente")
        else:
            resultado = generar_parley(picks)
            if resultado:
                guardar_parley(resultado)
                print(f"✅ Parley generado: {len(resultado['picks'])} picks.")
                guardar_log(len(resultado["picks"]), "generado")
            else:
                print("❌ No se pudo generar un parley que cumpla las reglas.")
                guardar_log(len(picks), "no_apto")
    except Exception as e:
        print(f"❌ Error al generar parley: {e}")
        guardar_log(0, f"error: {str(e)}")
