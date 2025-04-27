# scripts/enriquecer_partidos.py

import pandas as pd
import sqlite3
from datetime import datetime

# ⚙️ Ruta de la base de datos
db_path = "database/partidos.db"

# 📥 Cargar CSVs separados por año
batters_dfs = {
    2023: pd.read_csv("data/batters_team_2023.csv"),
    2024: pd.read_csv("data/batters_team_2024.csv"),
    2025: pd.read_csv("data/batters_team_2025.csv")
}

# 🔥 Limpiar nombres de equipos
for df in batters_dfs.values():
    df['team'] = df['team'].str.strip()

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

    if year not in batters_dfs:
        print(f"⚠️ Año {year} no disponible en los CSVs, saltando partido ID {partido_id}")
        continue

    # Seleccionar dataframe correcto
    batters_df = batters_dfs[year]

    # Buscar estadísticas locales y visitantes
    stats_local = batters_df[batters_df['team'] == local]
    stats_visitante = batters_df[batters_df['team'] == visitante]

    if not stats_local.empty and not stats_visitante.empty:
        try:
            cursor.execute('''
                UPDATE partidos
                SET
                    slg_local = ?,
                    woba_local = ?,
                    slg_visitante = ?,
                    woba_visitante = ?
                WHERE id = ?
            ''', (
                stats_local['slg'].values[0],
                stats_local['woba'].values[0],
                stats_visitante['slg'].values[0],
                stats_visitante['woba'].values[0],
                partido_id
            ))
        except Exception as e:
            print(f"❌ Error actualizando partido {partido_id}: {e}")

# 🛠️ Guardar cambios
conn.commit()
conn.close()

print("🎯 ¡Partidos enriquecidos correctamente!")
