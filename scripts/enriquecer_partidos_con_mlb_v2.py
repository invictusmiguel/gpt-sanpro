# scripts/enriquecer_partidos_con_mlb_v2.py

import pandas as pd
import sqlite3
from datetime import datetime

# ⚙️ Ruta de la base de datos
db_path = "database/partidos.db"

# 📥 Cargar CSVs de bateo y pitcheo usando el separador correcto
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

# 🔥 Limpiar espacios en los nombres de equipos
for df in batting_dfs.values():
    df['TEAM'] = df['TEAM'].str.strip()

for df in pitching_dfs.values():
    df['TEAM'] = df['TEAM'].str.strip()

# 🛠️ Conectar a la base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 📋 Leer los partidos existentes
cursor.execute("SELECT id, fecha, equipo_local, equipo_visitante FROM partidos")
partidos = cursor.fetchall()

# 📋 Mapeo de nombres de equipos para corregir diferencias
nombre_equipo_map = {
    "New York Yankees": "Yankees",
    "Cleveland Guardians": "Guardians",
    "Detroit Tigers": "Tigers",
    "Minnesota Twins": "Twins",
    "St. Louis Cardinals": "Cardinals",
    "Colorado Rockies": "Rockies",
    "Washington Nationals": "Nationals",
    "Fake Yankees": "Yankees",   # pruebas
    "Fake Red Sox": "Red Sox",    # pruebas
    "Toronto Blue Jays": "Blue Jays",
    "Boston Red Sox": "Red Sox",
    "Baltimore Orioles": "Orioles",
    "Los Angeles Angels": "Angels",
    "Milwaukee Brewers": "Brewers",
    "Cincinnati Reds": "Reds",
    "New York Mets": "Mets"
}

print(f"🔹 Enriqueciendo {len(partidos)} partidos...")

# 🚀 Procesar cada partido
for partido in partidos:
    partido_id, fecha, local, visitante = partido

    # Obtener el año del partido
    try:
        year = datetime.strptime(fecha, "%Y-%m-%d").year
    except Exception as e:
        print(f"⚠️ Error parseando fecha de partido ID {partido_id}: {fecha}")
        continue

    # Verificar que haya datos de ese año
    if year not in batting_dfs or year not in pitching_dfs:
        print(f"⚠️ Año {year} no disponible en los CSVs, saltando partido ID {partido_id}")
        continue

    # Aplicar el mapeo de nombres si existe
    local_corr = nombre_equipo_map.get(local, local)
    visitante_corr = nombre_equipo_map.get(visitante, visitante)

    # Seleccionar los dataframes correctos
    batting_df = batting_dfs[year]
    pitching_df = pitching_dfs[year]

    # Buscar estadísticas del equipo local
    stats_batting_local = batting_df[batting_df['TEAM'] == local_corr]
    stats_pitching_local = pitching_df[pitching_df['TEAM'] == local_corr]

    # Buscar estadísticas del equipo visitante
    stats_batting_visitante = batting_df[batting_df['TEAM'] == visitante_corr]
    stats_pitching_visitante = pitching_df[pitching_df['TEAM'] == visitante_corr]

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
    else:
        print(f"⚠️ Datos no encontrados para partido ID {partido_id}: {local_corr} vs {visitante_corr}")

# 🛠️ Guardar los cambios en la base de datos
conn.commit()
conn.close()

print("🎯 ¡Partidos enriquecidos correctamente con mapeo de nombres!")
