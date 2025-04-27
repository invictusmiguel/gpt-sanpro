# scripts/verificar_datos_partidos_v3.py

import sqlite3
import pandas as pd

# ⚙️ Ruta de la base de datos
db_path = "database/partidos.db"

# 🛠️ Conectar a la base de datos
conn = sqlite3.connect(db_path)

# 📋 Leer partidos con los campos enriquecidos
query = """
SELECT
    id,
    fecha,
    equipo_local,
    equipo_visitante,
    obp_local,
    slg_local,
    era_pitcher_local,
    obp_visitante,
    slg_visitante,
    era_pitcher_visitante
FROM partidos
ORDER BY fecha ASC
LIMIT 20
"""
partidos = pd.read_sql_query(query, conn)

# 🖨️ Mostrar los partidos en pantalla
print("\n🎯 Partidos enriquecidos (v3):")
print(partidos.to_string(index=False))

# 🚪 Cerrar la conexión
conn.close()
