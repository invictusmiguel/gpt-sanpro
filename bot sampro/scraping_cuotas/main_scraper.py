import json
import datetime
import traceback
from bots.oddspedia_scraper import get_odds_oddspedia

OUTPUT_FILE = "data/cuotas_mlbbulk.json"
LOG_FILE = "logs/scraping_log.csv"

def log_execution(success=True, error=""):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "OK" if success else "ERROR"
    row = f"{now},{status},{error}\n"

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(row)
    except Exception as e:
        print(f"⚠️ No se pudo escribir el log: {e}")

def main():
    print("🚀 Ejecutando scraper de Oddspedia...")

    try:
        odds_oddspedia = get_odds_oddspedia()
        print(f"🎯 Partidos encontrados: {len(odds_oddspedia)}")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(odds_oddspedia, f, indent=2, ensure_ascii=False)

        print(f"✅ Cuotas guardadas en {OUTPUT_FILE}")
        log_execution(success=True)

    except Exception as e:
        print("❌ Error en la ejecución del scraper.")
        traceback.print_exc()
        log_execution(success=False, error=str(e))

if __name__ == "__main__":
    main()
