# scripts/actualizar_resultados_partidos.py

import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('database/partidos.db')
cursor = conn.cursor()

# Actualizar algunos resultados manualmente
partidos_actualizados = [
    (5, 3, 2),  # ID 2: Yankees 5 - Blue Jays 3
    (2, 4, 3),  # ID 3: Guardians 2 - Red Sox 4
    (3, 2, 5),  # ID 5: Tigers 3 - Orioles 2
    (4, 1, 7),  # ID 7: Twins 4 - Angels 1
    (6, 5, 9),  # ID 9: Rockies 6 - Reds 5
    (2, 3, 10), # ID 10: Nationals 2 - Mets 3
    (3, 1, 11), # ID 11: Giants 3 - Rangers 1
    (5, 2, 12), # ID 12: Cubs 5 - Phillies 2
    (1, 4, 13), # ID 13: Athletics 1 - White Sox 4
]

for resultado_local, resultado_visitante, partido_id in partidos_actualizados:
    cursor.execute('''
        UPDATE partidos
        SET resultado_local = ?, resultado_visitante = ?
        WHERE id = ?
    ''', (resultado_local, resultado_visitante, partido_id))

# Guardar cambios
conn.commit()
conn.close()

print("🎯 Resultados actualizados correctamente en partidos.db!")
