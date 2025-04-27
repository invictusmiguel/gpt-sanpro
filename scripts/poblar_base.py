# scripts/poblar_base.py
import sqlite3
import os

os.makedirs("database", exist_ok=True)
conn = sqlite3.connect("database/partidos.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS partidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    equipo_local TEXT,
    equipo_visita TEXT,
    goles_local INTEGER,
    goles_visita INTEGER,
    cuota_local REAL,
    cuota_visitante REAL,
    acierto BOOLEAN
)
""")

conn.commit()
conn.close()
print("✅ Base de datos creada o actualizada correctamente.")
