import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://baseballsavant.mlb.com"

# Busca el perfil de un jugador por nombre
def buscar_url_savant(nombre):
    try:
        query = nombre.replace(" ", "+")
        search_url = f"{BASE_URL}/search?search={query}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Encuentra el primer resultado relevante
        links = soup.select('a[href^="/player/"]')
        if links:
            href = links[0]["href"]
            if "/player/" in href:
                return BASE_URL + href
        return None
    except Exception as e:
        print(f"❌ Error buscando URL de Savant para {nombre}: {e}")
        return None

# Recorre una lista de picks y le agrega el link de Savant si no lo tiene
def enriquecer_con_savant(picks):
    for pick in picks:
        partido = pick.get("partido", "")
        if "vs" in partido:
            equipos = partido.split(" vs ")
            if len(equipos) == 2:
                pitcher_local = pick.get("pitcher_local")
                pitcher_visitante = pick.get("pitcher_visitante")

                # Buscar Savant URL solo si no existe aún
                if pitcher_local and not pick.get("savant_local"):
                    pick["savant_local"] = buscar_url_savant(pitcher_local)
                    time.sleep(1)

                if pitcher_visitante and not pick.get("savant_visitante"):
                    pick["savant_visitante"] = buscar_url_savant(pitcher_visitante)
                    time.sleep(1)
    return picks
