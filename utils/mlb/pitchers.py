# utils/mlb/pitchers.py

import requests
from datetime import datetime

# Normaliza nombres comunes de equipos
equivalencias = {
    "NY Yankees": "New York Yankees",
    "CLE Guardians": "Cleveland Guardians",
    "CIN Reds": "Cincinnati Reds",
    "MIA Marlins": "Miami Marlins",
    "SD Padres": "San Diego Padres",
    "DET Tigers": "Detroit Tigers",
    "BAL Orioles": "Baltimore Orioles",
    "WAS Nationals": "Washington Nationals"
}

def normalizar(nombre):
    return equivalencias.get(nombre, nombre)

def get_pitchers_por_partido(partido, fecha=None):
    if not fecha:
        fecha = datetime.now().strftime("%Y-%m-%d")

    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={fecha}"
    res = requests.get(url)

    if res.status_code != 200:
        return {"error": "❌ No se pudo acceder a MLB API"}

    data = res.json().get('dates', [])
    if not data:
        return {"error": "⚠️ No hay partidos programados para hoy"}

    equipos_partido = partido.split(" vs ")
    equipo1 = normalizar(equipos_partido[0].strip())
    equipo2 = normalizar(equipos_partido[1].strip())

    for game in data[0].get("games", []):
        equipos = game['teams']
        home = equipos['home']['team']['name']
        away = equipos['away']['team']['name']

        if equipo1 in (home, away) and equipo2 in (home, away):
            pitcher_home = equipos['home'].get('probablePitcher', {}).get('fullName', 'N/D')
            pitcher_away = equipos['away'].get('probablePitcher', {}).get('fullName', 'N/D')

            return {
                "pitcher_local": pitcher_home if home == equipo1 else pitcher_away,
                "pitcher_visitante": pitcher_away if home == equipo1 else pitcher_home,
                "equipo_local": home,
                "equipo_visitante": away
            }

    return {"error": f"No se encontró el partido '{partido}' para hoy"}
