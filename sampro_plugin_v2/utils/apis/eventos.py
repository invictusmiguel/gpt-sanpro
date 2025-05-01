import requests
import json

API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

def obtener_eventos(fixture_id):
    url = f"https://v3.football.api-sports.io/fixtures/events?fixture={fixture_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        print("📺 EVENTOS DATA:")
        print(json.dumps(data, indent=2))

        return data
    except Exception as e:
        return {"error": str(e)}
