import os
import json
from datetime import datetime

ARCHIVO_BANCA = "banca.json"
HISTORIAL_PATH = "data/historial.json"

def inicializar_banca():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(ARCHIVO_BANCA):
        with open(ARCHIVO_BANCA, "w", encoding="utf-8") as f:
            json.dump({"saldo": 100.0, "historial": []}, f, indent=2)
    if not os.path.exists(HISTORIAL_PATH):
        with open(HISTORIAL_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

def leer_saldo():
    if not os.path.exists(ARCHIVO_BANCA):
        inicializar_banca()
    try:
        with open(ARCHIVO_BANCA, "r", encoding="utf-8") as f:
            return json.load(f)["saldo"]
    except:
        return 100.0

def registrar_en_historial(fixture_id, probabilidad, cuota, acertado):
    entrada = {
        "fecha": datetime.now().isoformat(),
        "fixture_id": fixture_id,
        "probabilidad": probabilidad,
        "cuota": cuota,
        "acertado": acertado
    }
    try:
        with open(HISTORIAL_PATH, "r", encoding="utf-8") as f:
            historial = json.load(f)
    except:
        historial = []

    historial.append(entrada)

    with open(HISTORIAL_PATH, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2)

    return "📈 Historial actualizado"

def registrar_apuesta(fixture_id, probabilidad, cuota, acierto):
    saldo = leer_saldo()
    inversion = saldo * 0.012
    ganancia = inversion * (cuota - 1) if acierto else -inversion
    nuevo_saldo = round(saldo + ganancia, 2)

    try:
        with open(ARCHIVO_BANCA, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {"saldo": 100.0, "historial": []}

    data["saldo"] = nuevo_saldo
    data["historial"].append({
        "fecha": datetime.now().isoformat(),
        "fixture_id": fixture_id,
        "probabilidad": probabilidad,
        "cuota": cuota,
        "apostado": round(inversion, 2),
        "resultado": "ganada" if acierto else "perdida",
        "ganancia": round(ganancia, 2),
        "nuevo_saldo": nuevo_saldo
    })

    with open(ARCHIVO_BANCA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    registrar_en_historial(fixture_id, probabilidad, cuota, acierto)

    verificar_y_recargar_banca()
    return f"💰 Nueva banca: {nuevo_saldo} PEN"

def verificar_y_recargar_banca():
    from datetime import datetime
    if not os.path.exists(ARCHIVO_BANCA):
        inicializar_banca()

    with open(ARCHIVO_BANCA, "r") as f:
        try:
            data = json.load(f)
        except:
            data = {"saldo": 0.0, "historial": []}

    saldo = data.get("saldo", 0.0)

    if saldo < 0.5:
        data["saldo"] += 100
        data["historial"].append({
            "fecha": datetime.now().isoformat(),
            "tipo": "recarga",
            "monto": 100,
            "razon": "Saldo agotado"
        })

        with open(ARCHIVO_BANCA, "w") as f:
            json.dump(data, f, indent=2)

        print("⚠️ Saldo agotado. Recarga de 100 PEN realizada.")
