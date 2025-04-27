# scripts/train_model_p2.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# 🚀 Cargar dataset
dataset_path = "data/dataset_entrenamiento.csv"

if not os.path.exists(dataset_path):
    print(f"❌ Error: No se encontró el archivo {dataset_path}")
    exit()

df = pd.read_csv(dataset_path)

# 🚀 Definir características (X) y etiqueta (y)
X = df[['slg_local', 'woba_local', 'obp_visitante', 'slg_visitante', 'woba_visitante',
        'era_pitcher_local', 'fip_pitcher_local', 'era_pitcher_visitante', 'fip_pitcher_visitante',
        'obp_diff', 'slg_diff', 'woba_diff', 'era_diff', 'fip_diff', 'diferencial_carreras']]

# 🎯 La etiqueta a predecir es el equipo ganador
y = df['equipo_ganador']

# 🚀 Dividir dataset en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🚀 Crear el modelo Random Forest
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# 🚀 Guardar el modelo entrenado
os.makedirs("models", exist_ok=True)
with open("models/modelo.pkl", "wb") as f:
    pickle.dump(modelo, f)

print("✅ Modelo entrenado y guardado en models/modelo.pkl")
