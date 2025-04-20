import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# Conectar a la base de datos
conn = sqlite3.connect('database/partidos.db')
df = pd.read_sql_query("SELECT * FROM partidos WHERE goles_local >= 0 AND goles_visita >= 0", conn)
conn.close()

# Preparar etiquetas y variables de entrada
df['local_es_ganador'] = (df['resultado'] == 'L').astype(int)
df['dif_goles'] = df['goles_local'] - df['goles_visita']

# Definir variables X (features) y y (target)
X = df[['goles_local', 'goles_visita', 'dif_goles']]
y = df['local_es_ganador']

# Dividir en entrenamiento y test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo
modelo = LogisticRegression()
modelo.fit(X_train, y_train)

# Evaluar exactitud
accuracy = modelo.score(X_test, y_test)
print(f"✅ Modelo entrenado con exactitud: {round(accuracy * 100, 2)}%")

# Guardar el modelo
joblib.dump(modelo, 'models/modelo_predictivo.pkl')
print("💾 Modelo guardado en: models/modelo_predictivo.pkl")
