import requests
import json

API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

def obtener_cuotas(fixture_id):
    url = f"https://v3.football.api-sports.io/odds?fixture={fixture_id}&bookmaker=1"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        print("💰 CUOTAS RAW DATA:")
        print(json.dumps(data, indent=2))

        if not data["response"]:
            return {"error": "No hay cuotas disponibles"}

        bookmaker_data = data["response"][0]["bookmaker"]
        casa = bookmaker_data["name"]

        for apuesta in bookmaker_data["bets"]:
            if apuesta["name"] == "Match Winner":
                opciones = apuesta["values"]
                return {
                    "casa": casa,
                    "local": float(opciones[0]["odd"]),
                    "empate": float(opciones[1]["odd"]),
                    "visitante": float(opciones[2]["odd"])
                }

        return {"error": "No se encontró el mercado 'Match Winner'"}

    except Exception as e:
        return {"error": str(e)}
