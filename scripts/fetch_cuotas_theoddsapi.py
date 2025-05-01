# 📦 Librerías necesarias
import requests
import json
import csv
from datetime import datetime
from pathlib import Path

# 🔑 API Key de TheOddsAPI (reemplazable por variable de entorno si se desea)
API_KEY = '023e83bb7d6624022be2cdc67eeb5f31'

# 🌍 Endpoint de cuotas MLB
url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"

# 📥 Parámetros de consulta
params = {
    'regions': 'us',
    'markets': 'h2h',
    'oddsFormat': 'decimal',
    'apiKey': API_KEY
}

# ✅ Función principal del script
def fetch_cuotas():
    try:
        print("📡 Conectando a TheOddsAPI...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            print("⚠️ No se recibieron datos desde la API.")
            return

        # 🎯 Formato limpio para SAMPRO
        cuotas_limpias = []
        for partido in data:
            if len(partido.get("bookmakers", [])) == 0:
                continue

            try:
                info = partido["bookmakers"][0]["markets"][0]["outcomes"]
                if len(info) < 2:
                    continue

                cuotas_limpias.append({
                    "evento": f"{info[0]['name']} vs {info[1]['name']}",
                    "fecha": partido["commence_time"][:10],
                    "equipo_local": info[0]['name'],
                    "equipo_visitante": info[1]['name'],
                    "cuota_local": float(info[0]['price']),
                    "cuota_visitante": float(info[1]['price'])
                })
            except Exception as e:
                print(f"❌ Error procesando un partido: {e}")

        # 📁 Guardar como JSON
        Path("data").mkdir(exist_ok=True)
        with open("data/cuotas_mlbbulk.json", "w", encoding="utf-8") as f:
            json.dump(cuotas_limpias, f, ensure_ascii=False, indent=2)

        print(f"✅ {len(cuotas_limpias)} partidos guardados en data/cuotas_mlbbulk.json")

        # 📝 Guardar log en CSV
        Path("logs").mkdir(exist_ok=True)
        with open("logs/cuotas_real_log.csv", "a", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([now, len(cuotas_limpias), "OK"])

    except Exception as e:
        print(f"❌ Error general: {str(e)}")

# 🚀 Ejecutar solo si se llama directamente
if __name__ == "__main__":
    fetch_cuotas()
