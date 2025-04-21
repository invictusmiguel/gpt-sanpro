import os
import json
import requests
from datetime import datetime

API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

DATA_DIR = "data_diaria"
OUTPUT_FILE = "database/resultados.json"

def obtener_resultado_real(fixture_id):
    url = f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
    try:
        res = requests.get(url, headers=HEADERS)
        data = res.json()["response"]
        if not data:
            return None

        match = data[0]
        goles_local = match["goals"]["home"]
        goles_visitante = match["goals"]["away"]
        estado = match["fixture"]["status"]["short"]

        return {
            "fixture_id": fixture_id,
            "estado": estado,
            "goles_local": goles_local,
            "goles_visitante": goles_visitante,
            "fecha": match["fixture"]["date"]
        }
    except Exception as e:
        return {"error": str(e)}

def guardar_resultados():
    resultados = []

    for archivo in os.listdir(DATA_DIR):
        if archivo.endswith(".json"):
            partes = archivo.split("_")
            if len(partes) < 3:
                continue
            try:
                fixture_id = int(partes[3].split(".")[0])
                resultado = obtener_resultado_real(fixture_id)
                if resultado:
                    resultados.append(resultado)
                    print(f"✔️ Resultado guardado: {fixture_id}")
            except:
                continue

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Resultados guardados en: {OUTPUT_FILE}")

if __name__ == "__main__":
    guardar_resultados()
