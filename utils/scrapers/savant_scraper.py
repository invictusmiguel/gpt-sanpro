import requests
from bs4 import BeautifulSoup

def get_pitcher_savant_stats(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        tabla = soup.find("div", id="statcast_stats_pitching")
        if not tabla:
            return {"error": "❌ No se encontró la tabla esperada de estadísticas"}

        tabla = tabla.find("table")
        if not tabla:
            return {"error": "❌ No se encontró la tabla dentro del div"}

        stats = {}

        # Recorremos todas las filas hasta encontrar una válida
        for row in tabla.find_all("tr")[1:]:
            celdas = row.find_all("td")
            if not celdas or len(celdas) < 21:
                continue  # Ignorar filas vacías o incompletas

            try:
                stats["xERA"] = float(celdas[20].text.strip()) if celdas[20].text.strip() else None
                stats["CSW%"] = float(celdas[18].text.strip()) if celdas[18].text.strip() else None
                stats["Whiff%"] = float(celdas[17].text.strip()) if celdas[17].text.strip() else None
                stats["Barrel%"] = float(celdas[5].text.strip()) if celdas[5].text.strip() else None
                stats["HardHit%"] = float(celdas[16].text.strip()) if celdas[16].text.strip() else None
                break  # Solo queremos la fila más reciente válida
            except Exception as e:
                print(f"⚠️ Error al convertir valores: {e}")
                continue

        if not stats:
            return {"error": "❌ No se encontraron estadísticas válidas"}

        return stats

    except Exception as e:
        return {"error": f"❌ Error general en Savant: {str(e)}"}
