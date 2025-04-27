# etl_baseball_api.py

import requests
import sqlite3
import pandas as pd
import os
from datetime import datetime

# 🧠 Función para obtener los partidos reales de hoy
def get_today_games():
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}"
    response = requests.get(url)
    data = response.json()

    games = []
    for date in data.get('dates', []):
        for game in date.get('games', []):
            games.append({
                "fecha": today,
                "equipo_local": game['teams']['home']['team']['name'],
                "equipo_visitante": game['teams']['away']['team']['name'],
                "resultado_local": game['teams']['home'].get('score', 0),
                "resultado_visitante": game['teams']['away'].get('score', 0),
                "estadio": game.get('venue', {}).get('name', 'Desconocido'),
                "clima": "N/A"  # No proporciona clima en este endpoint
            })
    return games

# 🔍 Simular stats para completar campos obligatorios
def enrich_game_data(game):
    enriched = {
        "fecha": game['fecha'],
        "equipo_local": game['equipo_local'],
        "equipo_visitante": game['equipo_visitante'],
        "obp_local": 0.330,
        "slg_local": 0.420,
        "woba_local": 0.340,
        "obp_visitante": 0.320,
        "slg_visitante": 0.410,
        "woba_visitante": 0.330,
        "era_pitcher_local": 3.50,
        "fip_pitcher_local": 3.80,
        "era_pitcher_visitante": 4.10,
        "fip_pitcher_visitante": 3.90,
        "estadio": game['estadio'],
        "clima": game['clima'],
        "resultado_local": game['resultado_local'],
        "resultado_visitante": game['resultado_visitante']
    }
    return enriched

# 💾 Función para guardar en SQLite
def save_to_db(data):
    conn = sqlite3.connect("database/partidos.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS partidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            equipo_local TEXT,
            equipo_visitante TEXT,
            obp_local REAL,
            slg_local REAL,
            woba_local REAL,
            obp_visitante REAL,
            slg_visitante REAL,
            woba_visitante REAL,
            era_pitcher_local REAL,
            fip_pitcher_local REAL,
            era_pitcher_visitante REAL,
            fip_pitcher_visitante REAL,
            estadio TEXT,
            clima TEXT,
            resultado_local INTEGER,
            resultado_visitante INTEGER
        );
    ''')
    placeholders = ', '.join(['?'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO partidos ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, list(data.values()))
    conn.commit()
    conn.close()
    print("✅ Datos guardados en la base de datos.")

# 📁 Función para guardar en CSV
def save_to_csv(data, path="data/partidos_etl.csv"):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    file_exists = os.path.isfile(path)
    df = pd.DataFrame([data])
    df.to_csv(path, mode='a', index=False, header=not file_exists)
    print(f"✅ CSV actualizado correctamente en: {path}")

# 🚀 Función principal del ETL
def run_etl():
    print("🔹 Iniciando script ETL usando API MLB...")
    print(f"🔹 Configuración:")
    print(f"- DB: {os.path.abspath('database/partidos.db')}")
    print(f"- CSV: {os.path.abspath('data')}")
    print("🔹 Obteniendo partidos de hoy...")

    games = get_today_games()

    if not games:
        print("⚠️ No se encontraron partidos para hoy.")
        return

    for game in games:
        enriched_game = enrich_game_data(game)
        save_to_db(enriched_game)
        save_to_csv(enriched_game)

    print("✅ Script completado exitosamente!")

# 🧠 Ejecutar si corre como principal
if __name__ == "__main__":
    run_etl()
