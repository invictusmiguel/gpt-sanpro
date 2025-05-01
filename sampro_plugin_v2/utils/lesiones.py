import requests

API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
BASE_URL = "https://v3.football.api-sports.io/injuries"

HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

def obtener_lesiones(team_id, season=2023):
    url = f"{BASE_URL}?season={season}&team={team_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        jugadores = []
        for item in data["response"]:
            jugador = item["player"]["name"]
            motivo = item["player"].get("reason", "sin motivo especificado")
            fecha = item.get("fixture", {}).get("date", "fecha no disponible")
            jugadores.append(f"{jugador} ({motivo}) - {fecha}")

        return jugadores or ["Sin lesiones registradas"]
    except Exception as e:
        return [f"Error: {str(e)}"]
