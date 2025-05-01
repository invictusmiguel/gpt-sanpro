# utils/scrapers/auto_savant.py
from utils.scrapers.savant_scraper import get_pitcher_savant_stats

def enriquecer_con_savant(picks):
    for pick in picks:
        for lado in ["savant_local", "savant_visitante"]:
            url = pick.get(lado)
            if url:
                stats = get_pitcher_savant_stats(url)
                if isinstance(stats, dict) and "error" not in stats:
                    # Insertamos estadísticas relevantes
                    pick[f"{lado}_xERA"] = stats.get("xERA")
                    pick[f"{lado}_CSW"] = stats.get("CSW%")
                    pick[f"{lado}_Whiff"] = stats.get("Whiff%")
                    pick[f"{lado}_Barrel"] = stats.get("Barrel%")
                    pick[f"{lado}_HardHit"] = stats.get("HardHit%")
                else:
                    print(f"⚠️ Error al obtener Savant desde {url}: {stats.get('error', 'desconocido')}")
            else:
                print(f"🔍 No hay URL Savant para {lado} en el pick: {pick.get('partido')}")
    return picks
