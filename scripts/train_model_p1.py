# scripts/train_model_p1.py

import sqlite3
import pandas as pd
import os

# ⚙️ Crear carpeta data si no existe
os.makedirs('data', exist_ok=True)

# 📥 Leer la tabla 'partidos' desde la base de datos
conn = sqlite3.connect('database/partidos.db')
df = pd.read_sql_query("SELECT * FROM partidos", conn)
conn.close()

print(f"✅ {len(df)} partidos cargados desde la base de datos.")

# 🧹 Eliminar partidos con datos incompletos en campos clave
campos_obligatorios = [
    'obp_local', 'slg_local', 'woba_local',
    'obp_visitante', 'slg_visitante', 'woba_visitante',
    'era_pitcher_local', 'fip_pitcher_local',
    'era_pitcher_visitante', 'fip_pitcher_visitante',
    'resultado_local', 'resultado_visitante'
]

df = df.dropna(subset=campos_obligatorios)
print(f"✅ {len(df)} partidos después de eliminar filas con datos nulos.")

# 🧹 Eliminar partidos donde hubo empate
df = df[df['resultado_local'] != df['resultado_visitante']]
print(f"✅ {len(df)} partidos después de eliminar empates.")

# 🛠️ Crear variables derivadas (features)
df['obp_diff'] = df['obp_local'] - df['obp_visitante']
df['slg_diff'] = df['slg_local'] - df['slg_visitante']
df['woba_diff'] = df['woba_local'] - df['woba_visitante']
df['era_diff'] = df['era_pitcher_visitante'] - df['era_pitcher_local']
df['fip_diff'] = df['fip_pitcher_visitante'] - df['fip_pitcher_local']

# 🏁 Crear las variables de salida (targets)
df['diferencial_carreras'] = df['resultado_local'] - df['resultado_visitante']
df['equipo_ganador'] = df['resultado_local'] > df['resultado_visitante']
df['equipo_ganador'] = df['equipo_ganador'].astype(int)  # 1 = local gana, 0 = local pierde

# 💾 Guardar dataset preprocesado
output_path = 'data/dataset_entrenamiento.csv'
df.to_csv(output_path, index=False)

print(f"🎯 Dataset preprocesado guardado en {output_path}")
