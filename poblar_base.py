# scripts/poblar_base.py

import sqlite3
import requests
import pandas as pd
import os
from datetime import datetime, timedelta

# ⚙️ Conexión a la base de datos
db_path = "database/partidos.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 🔥 API pública MLB para sacar partidos
base_url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1"

# 🗓️ Rango de fechas (últimos 90 días)
today = datetime.today()
start_date = today - timedelta(days=90)

# 📥 Lista para acumular datos
partidos = []

print(f"🔹 Descargando partidos entre {start_date.date()} y {today.date()}...")

# 📦 Descargar día por día
for i in range(90):
    fecha = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
    response = requests.get(f"{base_url}&date={fecha}")
    if response.status_code == 200:
        data = response.json()
        games = data.get("dates", [])
        if games:
            for game in games[0].get("games", []):
                try:
                    partido = {
                        "fecha": game["gameDate"][:10],
                        "equipo_local": game["teams"]["home"]["team"]["name"],
                        "equipo_visitante": game["teams"]["away"]["team"]["name"],
                        "obp_local": round(0.300 + 0.05 * (i % 5), 3),  # ⚠️ Simulación ligera (falta scraping real)
                        "slg_local": round(0.400 + 0.05 * (i % 5), 3),
                        "woba_local": round(0.320 + 0.04 * (i % 5), 3),
                        "obp_visitante": round(0.295 + 0.05 * (i % 5), 3),
                        "slg_visitante": round(0.390 + 0.05 * (i % 5), 3),
                        "woba_visitante": round(0.310 + 0.04 * (i % 5), 3),
                        "era_pitcher_local": round(3.50 + (i % 4) * 0.25, 2),
                        "fip_pitcher_local": round(3.80 + (i % 4) * 0.20, 2),
                        "era_pitcher_visitante": round(3.60 + (i % 4) * 0.30, 2),
                        "fip_pitcher_visitante": round(3.90 + (i % 4) * 0.25, 2),
                        "estadio": game["venue"]["name"],
                        "clima": "Desconocido",
                        "resultado_local": game["teams"]["home"]["score"],
                        "resultado_visitante": game["teams"]["away"]["score"]
                    }
                    partidos.append(partido)
                except Exception as e:
                    print(f"⚠️ Error al procesar un partido: {e}")

# 📊 Convertir a DataFrame
df = pd.DataFrame(partidos)

# 🚀 Insertar en SQLite
print(f"✅ Insertando {len(df)} partidos en la base de datos...")

for index, row in df.iterrows():
    cursor.execute('''
        INSERT INTO partidos (
            fecha, equipo_local, equipo_visitante,
            obp_local, slg_local, woba_local,
            obp_visitante, slg_visitante, woba_visitante,
            era_pitcher_local, fip_pitcher_local,
            era_pitcher_visitante, fip_pitcher_visitante,
            estadio, clima, resultado_local, resultado_visitante
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['fecha'], row['equipo_local'], row['equipo_visitante'],
        row['obp_local'], row['slg_local'], row['woba_local'],
        row['obp_visitante'], row['slg_visitante'], row['woba_visitante'],
        row['era_pitcher_local'], row['fip_pitcher_local'],
        row['era_pitcher_visitante'], row['fip_pitcher_visitante'],
        row['estadio'], row['clima'], row['resultado_local'], row['resultado_visitante']
    ))

conn.commit()
conn.close()

print("🎯 ¡Base de datos actualizada exitosamente!")
