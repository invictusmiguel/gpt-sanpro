import requests
from bs4 import BeautifulSoup

def get_pitcher_stats_espn(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            return {"error": "❌ No se pudo acceder a la página de ESPN"}

        soup = BeautifulSoup(res.text, "lxml")
        tabla = soup.find_all("table")
        if not tabla:
            return {"error": "❌ No se encontró ninguna tabla"}

        filas = tabla[0].find_all("tr")
        for fila in filas[::-1]:  # Buscar desde la última temporada hacia arriba
            columnas = fila.find_all("td")
            if len(columnas) >= 8:
                try:
                    era = float(columnas[4].text.strip().replace(",", "."))
                    ip = float(columnas[6].text.strip().replace(",", "."))
                    so = int(columnas[7].text.strip())
                    whip = float(columnas[8].text.strip().replace(",", "."))
                    return {
                        "ERA": era,
                        "WHIP": whip,
                        "SO": so,
                        "IP": ip
                    }
                except:
                    continue
        return {"error": "❌ No se pudo extraer estadísticas válidas"}

    except Exception as e:
        return {"error": f"❌ Error inesperado: {str(e)}"}
