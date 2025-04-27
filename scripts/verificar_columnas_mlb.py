# scripts/verificar_columnas_mlb.py

import pandas as pd

archivos = [
    "data/batting_mlb_2023.csv",
    "data/batting_mlb_2024.csv",
    "data/batting_mlb_2025.csv",
    "data/PITCHERS_mlb_2023.csv",
    "data/PITCHERS_mlb_2024.csv",
    "data/PITCHERS_mlb_2025.csv"
]

for archivo in archivos:
    try:
        df = pd.read_csv(archivo)
        print(f"\n📄 {archivo}:")
        print(f"  Columnas: {list(df.columns)}")
    except Exception as e:
        print(f"❌ Error leyendo {archivo}: {e}")
