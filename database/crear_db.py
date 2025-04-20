import sqlite3

conn = sqlite3.connect('database/partidos.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS partidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    equipo_local TEXT,
    equipo_visita TEXT,
    goles_local INTEGER,
    goles_visita INTEGER,
    liga TEXT,
    resultado TEXT,
    clima TEXT,
    lesionados TEXT,
    cuota_local REAL,
    cuota_visita REAL,
    acierto INTEGER
)
''')

conn.commit()
conn.close()
print("✅ Base de datos y tabla 'partidos' creada exitosamente.")
