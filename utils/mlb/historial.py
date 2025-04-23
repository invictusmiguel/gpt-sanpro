# utils/mlb/historial.py

import requests
from datetime import datetime, timedelta

def get_historial_enfrentamientos(equipo1, equipo2):
    # Fecha actual y fecha hace 6 meses
    hoy = datetime.now().strftime("%Y-%m-%d")
    seis_meses_atras = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")

    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={seis_meses_atras}&endDate={hoy}&gameTypes=R"

    res = requests.get(url)
    if res.status_code != 200:
        return {"error": "No se pudo acceder a MLB API"}

    data = res.json().get("dates", [])
    historial = []
    total_carreras = 0

    for dia in data:
        for game in dia["games"]:
            equipos = game["teams"]
            home = equipos["home"]["team"]["name"]
            away = equipos["away"]["team"]["name"]

            if equipo1 in (home, away) and equipo2 in (home, away):
                game_id = game["gamePk"]
                detalle = get_detalle_partido(game_id)

                if detalle:
                    carreras_local = detalle["teams"]["home"]["score"]
                    carreras_visita = detalle["teams"]["away"]["score"]
                    total = carreras_local + carreras_visita
                    total_carreras += total
                    historial.append({
                        "fecha": game["gameDate"],
                        "home": home,
                        "away": away,
                        "carreras_local": carreras_local,
                        "carreras_visita": carreras_visita,
                        "total": total
                    })

    if not historial:
        return {"error": "No hay enfrentamientos recientes"}

    promedio = round(total_carreras / len(historial), 2)

    return {
        "enfrentamientos": historial,
        "promedio_carreras": promedio,
        "total_partidos": len(historial)
    }

def get_detalle_partido(game_id):
    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore"
    res = requests.get(url)

    if res.status_code != 200:
        return None

    return res.json()
