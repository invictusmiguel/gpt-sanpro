# scripts/enriquecer_partidos_con_mlb.py

import pandas as pd
import sqlite3
from datetime import datetime

# ⚙️ Ruta de la base de datos
db_path = "database/partidos.db"

# 📥 Cargar CSVs de batting
batting_dfs = {
    2023: pd.read_csv("data/batting_mlb_2023.csv", sep=";"),
    2024: pd.read_csv("data/batting_mlb_2024.csv", sep=";"),
    2025: pd.read_csv("data/batting_mlb_2025.csv", sep=";")
}

pitching_dfs = {
    2023: pd.read_csv("data/PITCHERS_mlb_2023.csv", sep=";"),
    2024: pd.read_csv("data/PITCHERS_mlb_2024.csv", sep=";"),
    2025: pd.read_csv("data/PITCHERS_mlb_2025.csv", sep=";")
}

# 🔥 Limpiar nombres de equipos
for df in batting_dfs.values():
    df['TEAM'] = df['TEAM'].str.strip()

for df in pitching_dfs.values():
    df['TEAM'] = df['TEAM'].str.strip()

# 🛠️ Conectar a la base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 📋 Leer partidos existentes
cursor.execute("SELECT id, fecha, equipo_local, equipo_visitante FROM partidos")
partidos = cursor.fetchall()

print(f"🔹 Enriqueciendo {len(partidos)} partidos...")

# 🚀 Procesar cada partido
for partido in partidos:
    partido_id, fecha, local, visitante = partido

    # Obtener año del partido
    try:
        year = datetime.strptime(fecha, "%Y-%m-%d").year
    except Exception as e:
        print(f"⚠️ Error parseando fecha de partido ID {partido_id}: {fecha}")
        continue

    if year not in batting_dfs or year not in pitching_dfs:
        print(f"⚠️ Año {year} no disponible en los CSVs, saltando partido ID {partido_id}")
        continue

    # Seleccionar dataframe correcto
    batting_df = batting_dfs[year]
    pitching_df = pitching_dfs[year]

    # Buscar estadísticas locales
    stats_batting_local = batting_df[batting_df['TEAM'] == local]
    stats_pitching_local = pitching_df[pitching_df['TEAM'] == local]

    # Buscar estadísticas visitantes
    stats_batting_visitante = batting_df[batting_df['TEAM'] == visitante]
    stats_pitching_visitante = pitching_df[pitching_df['TEAM'] == visitante]

    if not stats_batting_local.empty and not stats_batting_visitante.empty and not stats_pitching_local.empty and not stats_pitching_visitante.empty:
        try:
            cursor.execute('''
                UPDATE partidos
                SET
                    obp_local = ?,
                    slg_local = ?,
                    era_pitcher_local = ?,
                    obp_visitante = ?,
                    slg_visitante = ?,
                    era_pitcher_visitante = ?
                WHERE id = ?
            ''', (
                stats_batting_local['OBP'].values[0],
                stats_batting_local['SLG'].values[0],
                stats_pitching_local['ERA'].values[0],
                stats_batting_visitante['OBP'].values[0],
                stats_batting_visitante['SLG'].values[0],
                stats_pitching_visitante['ERA'].values[0],
                partido_id
            ))
        except Exception as e:
            print(f"❌ Error actualizando partido {partido_id}: {e}")

# 🛠️ Guardar cambios
conn.commit()
conn.close()

print("🎯 ¡Partidos enriquecidos correctamente con datos de MLB.com!")
