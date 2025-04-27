# scripts/verificar_datos_partidos.py

import sqlite3
import pandas as pd

# ⚙️ Ruta de la base de datos
db_path = "database/partidos.db"

# 🛠️ Conectar
conn = sqlite3.connect(db_path)

# 📋 Leer partidos enriquecidos
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
LIMIT 10
"""
partidos = pd.read_sql_query(query, conn)

# 🖨️ Mostrar algunos partidos
print("\n🎯 Partidos enriquecidos:")
print(partidos)

# 🚪 Cerrar conexión
conn.close()
