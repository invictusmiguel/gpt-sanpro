import subprocess
import requests
import json
import os

def ejecutar_scraper():
    print("🚀 Ejecutando scraper de cuotas...")
    # Ejecuta main_scraper.py desde la carpeta actual
    subprocess.run(["python", "main_scraper.py"], check=True)

def obtener_parleys():
    print("📡 Consultando endpoint /parley_seguro_vida...")
    try:
        res = requests.get("http://localhost:5000/parley_seguro_vida")
        parlays = res.json()

        if isinstance(parlays, list) and len(parlays) > 0:
            ruta_salida = "data/parleys_generados.json"
            os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
            with open(ruta_salida, "w", encoding="utf-8") as f:
                json.dump(parlays, f, indent=2, ensure_ascii=False)
            print(f"✅ Parlays guardados en {ruta_salida}")
        else:
            print("⚠️ No se generaron parlays válidos.")
    except Exception as e:
        print("❌ Error al consultar el endpoint:", str(e))


if __name__ == "__main__":
    ejecutar_scraper()
    obtener_parleys()
