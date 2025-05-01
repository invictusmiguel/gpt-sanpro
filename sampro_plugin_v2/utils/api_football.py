import requests
import os

def obtener_partidos_hoy():
    api_key = os.getenv("API_FOOTBALL_KEY")
    url = "https://v3.football.api-sports.io/fixtures?date=2025-04-20"

    headers = {
        "x-apisports-key": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data.get("response", [])  # Lista de partidos
    except Exception as e:
        return f"Error al obtener partidos: {e}"
