import os
import json
import requests
from datetime import datetime

# Configura tu clave
API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

# Directorio base para guardar los archivos
BASE_DIR = "data_diaria"
FECHA = datetime.today().strftime("%Y-%m-%d")
RUTA_DIA = os.path.join(BASE_DIR, FECHA)
os.makedirs(RUTA_DIA, exist_ok=True)

# Obtener fixtures del día
url = f"https://v3.football.api-sports.io/fixtures?date={FECHA}"

response = requests.get(url, headers=HEADERS)
fixtures = response.json().get("response", [])

print(f"📅 Se encontraron {len(fixtures)} partidos para hoy.")

for fixture in fixtures:
    fixture_id = fixture["fixture"]["id"]
    home = fixture["teams"]["home"]["name"]
    away = fixture["teams"]["away"]["name"]

    # Ahora obtén las cuotas del fixture
    odds_url = f"https://v3.football.api-sports.io/odds?fixture={fixture_id}&bookmaker=1"
    odds_response = requests.get(odds_url, headers=HEADERS)
    odds_data = odds_response.json()

    # Solo guardar si hay cuotas disponibles
    if odds_data.get("response"):
        nombre_archivo = f"{FECHA}_{fixture_id}_{home}_vs_{away}.json".replace(" ", "_")
        ruta_archivo = os.path.join(RUTA_DIA, nombre_archivo)

        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(odds_data, f, indent=2)

        print(f"✅ Archivo guardado: {nombre_archivo}")
    else:
        print(f"❌ Sin cuotas: {fixture_id} {home} vs {away}")
