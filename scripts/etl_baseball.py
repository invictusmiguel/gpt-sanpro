# scripts/etl_baseball.py

# 📦 Importaciones necesarias
import requests
import pandas as pd
import sqlite3
from datetime import datetime

# 📈 Función para extraer datos de partidos MLB
def extraer_datos():
    print("🔵 Extrayendo datos de partidos MLB...")

    url = "https://statsapi.mlb.com/api/v1/schedule"
    params = {
        "sportId": 1,
        "startDate": "2025-04-20",
        "endDate": "2025-04-25",
        "gameTypes": "R",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error al obtener datos de MLB: {e}")
        return pd.DataFrame()

    data = response.json()

    partidos = []
    for date_info in data.get("dates", []):
        for game in date_info.get("games", []):
            partido = {
                "fecha": game.get("gameDate", "").split("T")[0],
                "equipo_local": game.get("teams", {}).get("home", {}).get("team", {}).get("name", ""),
                "equipo_visitante": game.get("teams", {}).get("away", {}).get("team", {}).get("name", ""),
                "estadio": game.get("venue", {}).get("name", "")
            }
            partidos.append(partido)

    partidos_df = pd.DataFrame(partidos)

    print(f"✅ {len(partidos_df)} partidos extraídos de MLB.")
    return partidos_df

# 📚 Función para extraer sabermetría de bateo desde MLB API
def extraer_sabermetria_bateo_mlb():
    print("🔵 Extrayendo sabermetría de bateo desde MLB API...")

    url = "https://statsapi.mlb.com/api/v1/teams/stats?stats=season&group=hitting"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Error accediendo a MLB Stats API (bateo): {e}")
        return pd.DataFrame()

    equipos = []
    for team_stat in data.get('stats', [])[0].get('splits', []):
        equipo = {
            'equipo': team_stat.get('team', {}).get('name', '').lower(),
            'obp': float(team_stat.get('stat', {}).get('obp', 0)),
            'slg': float(team_stat.get('stat', {}).get('slg', 0)),
            'woba': float(team_stat.get('stat', {}).get('woba', 0)) if 'woba' in team_stat.get('stat', {}) else None
        }
        equipos.append(equipo)

    df_bateo = pd.DataFrame(equipos)

    print(f"✅ {len(df_bateo)} equipos extraídos desde MLB API (bateo).")
    return df_bateo
# 📚 Función para extraer sabermetría de pitcheo desde MLB API
def extraer_sabermetria_pitcheo_mlb():
    print("🔵 Extrayendo sabermetría de pitcheo desde MLB API...")

    url = "https://statsapi.mlb.com/api/v1/teams/stats?stats=season&group=pitching"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Error accediendo a MLB Stats API (pitcheo): {e}")
        return pd.DataFrame()

    equipos = []
    for team_stat in data.get('stats', [])[0].get('splits', []):
        equipo = {
            'equipo': team_stat.get('team', {}).get('name', '').lower(),
            'era': float(team_stat.get('stat', {}).get('era', 0)),
            'fip': float(team_stat.get('stat', {}).get('fip', 0)) if 'fip' in team_stat.get('stat', {}) else None
        }
        equipos.append(equipo)

    df_pitcheo = pd.DataFrame(equipos)

    print(f"✅ {len(df_pitcheo)} equipos extraídos desde MLB API (pitcheo).")
    return df_pitcheo


# 📚 Función para extraer sabermetría de pitcheo desde MLB API
def extraer_sabermetria_pitcheo_mlb():
    print("🔵 Extrayendo sabermetría de pitcheo desde MLB API...")

    url = "https://statsapi.mlb.com/api/v1/teams/stats?stats=season&group=pitching"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Error accediendo a MLB Stats API (pitcheo): {e}")
        return pd.DataFrame()

    equipos = []
    for team_stat in data.get('stats', [])[0].get('splits', []):
        equipo = {
            'equipo': team_stat.get('team', {}).get('name', '').lower(),
            'era': float(team_stat.get('stat', {}).get('era', 0)),
            'fip': float(team_stat.get('stat', {}).get('fip', 0)) if 'fip' in team_stat.get('stat', {}) else None
        }
        equipos.append(equipo)

    df_pitcheo = pd.DataFrame(equipos)

    print(f"✅ {len(df_pitcheo)} equipos extraídos desde MLB API (pitcheo).")
    return df_pitcheo
# 🔧 Función para transformar y unir todos los datos
def transformar_datos(df_partidos, df_bateo, df_pitcheo):
    print("🟠 Transformando y combinando todos los datos...")

    if df_partidos.empty or df_bateo.empty or df_pitcheo.empty:
        print("⚠️ No hay datos suficientes para transformar.")
        return pd.DataFrame()

    # Normalizar nombres
    df_partidos['equipo_local'] = df_partidos['equipo_local'].str.lower()
    df_partidos['equipo_visitante'] = df_partidos['equipo_visitante'].str.lower()
    df_partidos['estadio'] = df_partidos['estadio'].str.title()
    df_partidos['fecha'] = pd.to_datetime(df_partidos['fecha']).dt.strftime('%Y-%m-%d')

    # Unir datos de bateo
    df_partidos = df_partidos.merge(df_bateo, how='left', left_on='equipo_local', right_on='equipo')
    df_partidos = df_partidos.rename(columns={
        'obp': 'obp_local',
        'slg': 'slg_local',
        'woba': 'woba_local'
    }).drop(columns=['equipo'])

    df_partidos = df_partidos.merge(df_bateo, how='left', left_on='equipo_visitante', right_on='equipo')
    df_partidos = df_partidos.rename(columns={
        'obp': 'obp_visitante',
        'slg': 'slg_visitante',
        'woba': 'woba_visitante'
    }).drop(columns=['equipo'])

    # Unir datos de pitcheo
    df_partidos = df_partidos.merge(df_pitcheo, how='left', left_on='equipo_local', right_on='equipo')
    df_partidos = df_partidos.rename(columns={
        'era': 'era_pitcher_local',
        'fip': 'fip_pitcher_local'
    }).drop(columns=['equipo'])

    df_partidos = df_partidos.merge(df_pitcheo, how='left', left_on='equipo_visitante', right_on='equipo')
    df_partidos = df_partidos.rename(columns={
        'era': 'era_pitcher_visitante',
        'fip': 'fip_pitcher_visitante'
    }).drop(columns=['equipo'])

    print("✅ Todos los datos combinados correctamente.")
    return df_partidos

# 💾 Función para cargar los datos en SQLite
def cargar_datos(df):
    print("🟢 Cargando datos en la base de datos...")

    if df.empty:
        print("⚠️ No hay datos para cargar.")
        return

    conn = sqlite3.connect('database/partidos.db')
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

    for index, row in df.iterrows():
        cursor.execute('''
            INSERT INTO partidos (
                fecha, equipo_local, equipo_visitante,
                obp_local, slg_local, woba_local,
                obp_visitante, slg_visitante, woba_visitante,
                era_pitcher_local, fip_pitcher_local,
                era_pitcher_visitante, fip_pitcher_visitante,
                estadio
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['fecha'],
            row['equipo_local'],
            row['equipo_visitante'],
            row['obp_local'],
            row['slg_local'],
            row['woba_local'],
            row['obp_visitante'],
            row['slg_visitante'],
            row['woba_visitante'],
            row['era_pitcher_local'],
            row['fip_pitcher_local'],
            row['era_pitcher_visitante'],
            row['fip_pitcher_visitante'],
            row['estadio']
        ))

    conn.commit()
    conn.close()

    print(f"✅ {len(df)} partidos insertados en la base de datos.")

# 🏗️ Función principal de ETL
def main():
    print("🚀 Iniciando ETL de SAMPRO usando MLB API...")

    # 1. Extraer datos
    partidos_df = extraer_datos()
    sabermetria_bateo_df = extraer_sabermetria_bateo_mlb()
    sabermetria_pitcheo_df = extraer_sabermetria_pitcheo_mlb()

    # 2. Transformar datos
    partidos_limpios = transformar_datos(partidos_df, sabermetria_bateo_df, sabermetria_pitcheo_df)

    # 3. Cargar en la base de datos
    cargar_datos(partidos_limpios)

# 🚀 Ejecutar el script
if __name__ == "__main__":
    main()
