# utils/mlb/espn_scraper.py

import requests
from bs4 import BeautifulSoup

def get_stats_espn(nombre="garrett-cole", player_id="33039"):
    url = f"https://www.espn.com/mlb/player/stats/_/id/{player_id}/{nombre}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "❌ No se pudo acceder a la página de ESPN"}

    soup = BeautifulSoup(response.text, "lxml")

    try:
        tabla = soup.find("table")  # Encuentra la tabla de estadísticas
        filas = tabla.find_all("tr")

        for fila in filas:
            columnas = fila.find_all("td")
            if columnas and columnas[0].text.strip() == "2024":
                era = columnas[4].text.strip()   # ERA
                whip = columnas[6].text.strip()  # WHIP

                return {
                    "nombre": nombre.replace("-", " ").title(),
                    "ERA": era,
                    "WHIP": whip
                }

        return {"error": "⚠️ No se encontró información del año actual"}

    except Exception as e:
        return {"error": f"⚠️ Error al parsear datos: {str(e)}"}
