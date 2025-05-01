import joblib
import numpy as np

# Cargar el modelo entrenado
modelo = joblib.load('models/modelo_predictivo.pkl')

def predecir_resultado(goles_local, goles_visitante):
    dif_goles = goles_local - goles_visitante
    entrada = np.array([[goles_local, goles_visitante, dif_goles]])
    pred = modelo.predict_proba(entrada)[0]
    return {
        "probabilidad_gana_local": round(pred[1], 4),
        "probabilidad_no_gana_local": round(pred[0], 4)
    }
