# scripts/enriquecer_partidos_con_mlb_v3.py

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

print(f"🔹 Enriqueciendo {len(partidos)} partidos...")

# 🛠️ Función para buscar coincidencia inteligente
def buscar_equipo(df, nombre_equipo):
    nombre_equipo = str(nombre_equipo).lower()
    for equipo in df['TEAM']:
        equipo = str(equipo)  # Asegurarse que sea texto
        equipo_lower = equipo.lower()
        if nombre_equipo in equipo_lower or equipo_lower in nombre_equipo:
            return equipo
    return None


# 🚀 Procesar cada partido
for partido in partidos:
    partido_id, fecha, local, visitante = partido

    # Obtener el año del partido
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

    # Buscar equipos corregidos
    local_corr_batting = buscar_equipo(batting_df, local)
    visitante_corr_batting = buscar_equipo(batting_df, visitante)

    local_corr_pitching = buscar_equipo(pitching_df, local)
    visitante_corr_pitching = buscar_equipo(pitching_df, visitante)

    if all([local_corr_batting, visitante_corr_batting, local_corr_pitching, visitante_corr_pitching]):
        stats_batting_local = batting_df[batting_df['TEAM'] == local_corr_batting]
        stats_pitching_local = pitching_df[pitching_df['TEAM'] == local_corr_pitching]

        stats_batting_visitante = batting_df[batting_df['TEAM'] == visitante_corr_batting]
        stats_pitching_visitante = pitching_df[pitching_df['TEAM'] == visitante_corr_pitching]

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
        print(f"⚠️ No se encontró algún dato para partido ID {partido_id}: {local} vs {visitante}")

# 🛠️ Guardar cambios
conn.commit()
conn.close()

print("🎯 ¡Partidos enriquecidos correctamente usando búsqueda inteligente!")
