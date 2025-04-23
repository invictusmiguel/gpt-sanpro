# utils/scrapers/savant_scraper.py

import requests
from bs4 import BeautifulSoup

def get_pitcher_savant_stats(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            return {"error": "❌ No se pudo acceder a Baseball Savant"}

        soup = BeautifulSoup(res.text, "lxml")
        tabla = soup.find("table")

        if not tabla:
            return {"error": "❌ No se encontró tabla de métricas"}

        rows = tabla.find_all("tr")

        # Inicializamos variables con valores por defecto
        xera = csw = barrel = hard_hit = whiff = None

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                metrica = cols[0].text.strip().lower()
                valor = cols[1].text.strip().replace("%", "").replace(",", ".")

                try:
                    if "xera" in metrica:
                        xera = float(valor)
                    elif "csw" in metrica:
                        csw = float(valor)
                    elif "barrel" in metrica:
                        barrel = float(valor)
                    elif "hard hit" in metrica:
                        hard_hit = float(valor)
                    elif "whiff" in metrica:
                        whiff = float(valor)
                except ValueError:
                    continue

        if xera is None and csw is None and whiff is None:
            return {"error": "❌ No se encontraron métricas válidas"}

        return {
            "xERA": xera,
            "CSW%": csw,
            "Barrel%": barrel,
            "HardHit%": hard_hit,
            "Whiff%": whiff
        }

    except Exception as e:
        return {"error": f"❌ Error inesperado: {str(e)}"}
