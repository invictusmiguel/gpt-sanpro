# utils/apis/resultados.py
import requests

API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

def resultado_real(fixture_id):
    url = f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
    try:
        res = requests.get(url, headers=HEADERS)
        data = res.json()

        if not data["response"]:
            return {"error": "No se encontró el resultado"}

        fixture = data["response"][0]
        goles_local = fixture["goals"]["home"]
        goles_visita = fixture["goals"]["away"]

        return {"acertado": goles_local > goles_visita}
    
    except Exception as e:
        return {"error": str(e)}
