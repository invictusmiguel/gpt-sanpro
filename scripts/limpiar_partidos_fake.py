# scripts/limpiar_partidos_fake.py

import sqlite3

# ⚙️ Ruta de la base de datos
db_path = 'database/partidos.db'

# 🛠️ Conectar a la base
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 🧹 Ejecutar eliminación de partidos falsos
cursor.execute("DELETE FROM partidos WHERE equipo_local LIKE '%Fake%' OR equipo_visitante LIKE '%Fake%';")

# 💾 Guardar cambios
conn.commit()
conn.close()

print("🎯 ¡Partidos 'Fake' eliminados correctamente!")
