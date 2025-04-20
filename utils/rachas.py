import requests
import json
from collections import Counter

API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
BASE_URL = "https://v3.football.api-sports.io/fixtures"

HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

def obtener_racha(team_id):
    url = f"{BASE_URL}?team={team_id}&last=5"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        # 🔎 DEBUG: imprimimos en consola para análisis
        print("🔎 FIXTURES RAW RESPONSE:")
        print(json.dumps(data, indent=2))

        resultados = []
        goles_marcados = 0
        goles_recibidos = 0
        resumen_letras = []

        for match in data["response"]:
            local = match["teams"]["home"]["name"]
            visitante = match["teams"]["away"]["name"]
            marcador_local = match["goals"]["home"] or 0
            marcador_visitante = match["goals"]["away"] or 0
            es_local = (match["teams"]["home"]["id"] == team_id)

            if marcador_local > marcador_visitante:
                resultado = "W" if es_local else "L"
            elif marcador_local < marcador_visitante:
                resultado = "L" if es_local else "W"
            else:
                resultado = "D"

            resumen_letras.append(resultado)

            goles_marcados += marcador_local if es_local else marcador_visitante
            goles_recibidos += marcador_visitante if es_local else marcador_local

            resultados.append(
                f"{local} {marcador_local}-{marcador_visitante} {visitante} ➜ <b>{resultado}</b>"
            )

        conteo = Counter(resumen_letras)
        analisis = f"Racha: {conteo['W']} victorias, {conteo['D']} empates, {conteo['L']} derrotas"

        return {
            "racha": resultados,
            "goles_marcados": goles_marcados,
            "goles_recibidos": goles_recibidos,
            "resumen": analisis
        }

    except Exception as e:
        return {"error": str(e)}
