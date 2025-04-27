# scripts/train_model.py

import pandas as pd
import os
import joblib
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, roc_auc_score

# 🚀 Paso 1: Cargar dataset limpio
dataset_path = "data/dataset_entrenamiento.csv"

if not os.path.exists(dataset_path):
    print(f"❌ Error: No se encontró el archivo {dataset_path}")
    exit()

df = pd.read_csv(dataset_path)

print("✅ Dataset cargado exitosamente.")

# 🚀 Paso 2: Preparar Features y Targets
features = ['obp_diff', 'slg_diff', 'woba_diff', 'era_diff', 'fip_diff']
X = df[features]
y_regresion = df['diferencial_carreras']
y_clasificacion = df['equipo_ganador']

# 🚀 Paso 3: Escalar las Features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Guardar scaler
os.makedirs("models", exist_ok=True)
joblib.dump(scaler, 'models/scaler.pkl')
print("✅ Escalador guardado en models/scaler.pkl.")

# 🚀 Paso 4: División en Train/Test
X_train, X_test, y_train_reg, y_test_reg = train_test_split(
    X_scaled, y_regresion, test_size=0.2, random_state=42
)

_, _, y_train_clf, y_test_clf = train_test_split(
    X_scaled, y_clasificacion, test_size=0.2, random_state=42
)

print("✅ División en conjuntos de entrenamiento y prueba completada.")

# 🚀 Paso 5: Entrenamiento de Modelos

# Modelo de Regresión
modelo_regresion = RandomForestRegressor(
    n_estimators=100,
    max_depth=6,
    random_state=42
)
modelo_regresion.fit(X_train, y_train_reg)

# Modelo de Clasificación
modelo_clasificacion = RandomForestClassifier(
    n_estimators=100,
    max_depth=6,
    random_state=42
)
modelo_clasificacion.fit(X_train, y_train_clf)

print("✅ Modelos entrenados correctamente.")

# 🚀 Paso 6: Evaluación de Modelos

# Evaluación de Regresión
y_pred_reg = modelo_regresion.predict(X_test)
mae = mean_absolute_error(y_test_reg, y_pred_reg)
r2 = r2_score(y_test_reg, y_pred_reg)

print("\n🎯 Evaluación Modelo de Regresión:")
print(f"MAE (Error Medio Absoluto): {mae:.3f}")
print(f"R² (Coeficiente de Determinación): {r2:.3f}")

# Evaluación de Clasificación
y_pred_clf = modelo_clasificacion.predict(X_test)
y_proba_clf = modelo_clasificacion.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test_clf, y_pred_clf)
auc = roc_auc_score(y_test_clf, y_proba_clf)

print("\n🎯 Evaluación Modelo de Clasificación:")
print(f"Accuracy (Precisión): {accuracy:.3f}")
print(f"AUC-ROC Score: {auc:.3f}")

# 🚀 Paso 7: Guardado de Modelos
joblib.dump(modelo_regresion, 'models/modelo_regresion.pkl')
joblib.dump(modelo_clasificacion, 'models/modelo_clasificacion.pkl')

print("\n✅ Modelos guardados exitosamente en carpeta models/:")
print("- modelo_regresion.pkl")
print("- modelo_clasificacion.pkl")
print("- scaler.pkl")
