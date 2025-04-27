# scripts/scrapear_savant.py

import pandas as pd
import requests

def obtener_estadisticas_savant():
    print("🔹 Descargando estadísticas reales de Baseball Savant vía API interna...")

    url = "https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2024&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfInfield=&team=&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&metric_1=woba&sort_col=woba&sort_order=desc&min_pa=20"

    try:
        df = pd.read_csv(url)
        print(f"✅ {len(df)} registros de bateadores descargados.")
        
        # Agrupamos por equipo (hay equipos duplicados en nombres)
        equipos = df.groupby('team').mean()[["woba", "obp", "slg"]]

        equipos.reset_index(inplace=True)
        equipos.to_csv("data/equipos_savant.csv", index=False)
        
        print(f"✅ Equipos procesados y guardados en data/equipos_savant.csv")
        return equipos

    except Exception as e:
        print(f"❌ Error durante scraping: {e}")
        return None

if __name__ == "__main__":
    obtener_estadisticas_savant()
