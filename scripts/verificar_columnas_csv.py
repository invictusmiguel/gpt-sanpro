# scripts/verificar_columnas_csv.py

import pandas as pd

# ⚙️ Archivos a revisar
archivos = [
    "data/batters_team_2023.csv",
    "data/batters_team_2024.csv",
    "data/batters_team_2025.csv",
    "data/pitchers_team_2023.csv",
    "data/pitchers_team_2024.csv",
    "data/pitchers_team_2025.csv"
]

# 🔥 Revisar columnas
for archivo in archivos:
    try:
        df = pd.read_csv(archivo)
        print(f"\n📄 {archivo}:")
        print(f"  Columnas: {list(df.columns)}")
    except Exception as e:
        print(f"❌ Error leyendo {archivo}: {e}")
