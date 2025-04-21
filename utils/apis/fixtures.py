import requests
from datetime import datetime, timedelta
import requests
import os

API_KEY = os.getenv("API_FOOTBALL_KEY") or "cef9115ecad4dcadf30573ca8c3d3abe"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

def obtener_fixtures_del_dia():
    from datetime import date
    hoy = date.today().isoformat()

    url = f"https://v3.football.api-sports.io/fixtures?date={hoy}"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}


API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

def buscar_fixture_con_cuotas(liga_id=39):  # Liga Premier por defecto
    base_url = "https://v3.football.api-sports.io"
    fechas = [
        datetime.today().strftime('%Y-%m-%d'),
        (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    ]

    for fecha in fechas:
        fixtures_url = f"{base_url}/fixtures?league={liga_id}&season=2024&date={fecha}"
        try:
            resp = requests.get(fixtures_url, headers=HEADERS)
            fixtures = resp.json()["response"]
            for partido in fixtures:
                fixture_id = partido["fixture"]["id"]

                # Revisamos si hay cuotas para este partido
                odds_url = f"{base_url}/odds?fixture={fixture_id}&bookmaker=1"
                odds_resp = requests.get(odds_url, headers=HEADERS)
                odds_data = odds_resp.json()

                if odds_data["response"]:  # hay cuotas disponibles
                    return {
                        "fixture_id": fixture_id,
                        "local": partido["teams"]["home"]["name"],
                        "visitante": partido["teams"]["away"]["name"],
                        "fecha": partido["fixture"]["date"]
                    }

        except Exception as e:
            return {"error": str(e)}

    return {"error": "No se encontraron fixtures con cuotas"}
