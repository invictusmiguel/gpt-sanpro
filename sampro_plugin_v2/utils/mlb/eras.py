import requests
from datetime import datetime

def obtener_era_pitcher(nombre_pitcher):
    if not nombre_pitcher or nombre_pitcher in ["N/D", ""]:
        return None

    url = "https://statsapi.mlb.com/api/v1/people/search"
    params = {"name": nombre_pitcher}
    res = requests.get(url, params=params)

    if res.status_code != 200:
        return None

    data = res.json().get("people", [])
    if not data:
        return None

    pitcher_id = data[0]["id"]

    fecha = datetime.now().strftime("%Y-%m-%d")
    stats_url = f"https://statsapi.mlb.com/api/v1/people/{pitcher_id}/stats?stats=season&group=pitching&season=2024"
    stats_res = requests.get(stats_url)

    if stats_res.status_code != 200:
        return None

    stats = stats_res.json().get("stats", [])
    if stats:
        splits = stats[0].get("splits", [])
        if splits and "era" in splits[0].get("stat", {}):
            return float(splits[0]["stat"]["era"])

    return None
