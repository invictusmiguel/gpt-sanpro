import requests
import json

API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

def obtener_estadisticas(fixture_id, team_id):
    url = f"https://v3.football.api-sports.io/teams/statistics?fixture={fixture_id}&team={team_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        print("📊 ESTADÍSTICAS TEAM DATA:")
        print(json.dumps(data, indent=2))

        if "response" not in data or not isinstance(data["response"], dict):
            return {"error": "No hay estadísticas disponibles"}

        stats = data["response"].get("statistics", [])
        if not stats:
            return {"error": "No hay estadísticas disponibles"}

        resumen = []
        for stat in stats:
            tipo = stat.get("type")
            valor = stat.get("value")
            resumen.append(f"{tipo}: {valor}")

        return resumen

    except Exception as e:
        return {"error": str(e)}
