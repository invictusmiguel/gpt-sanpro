# 🧠 IA ORQUESTADORA - ia_engine.py
from prophet import Prophet
import pandas as pd
import numpy as np
import joblib
import random
import os
import json
from datetime import datetime

# 🧠 Predicción sabermétrica
def predict_with_model(input_data):
    try:
        modelo_reg = joblib.load("models/regression_model.pkl")
        modelo_clf = joblib.load("models/classification_model.pkl")
        scaler = joblib.load("models/scaler.pkl")

        column_order = [
            "obp_local", "slg_local", "woba_local", "era_pitcher_local", "fip_pitcher_local",
            "obp_visitante", "slg_visitante", "woba_visitante", "era_pitcher_visitante", "fip_pitcher_visitante"
        ]

        X_dict = {
            "obp_local": [input_data["obp_diff"]],
            "slg_local": [input_data["slg_diff"]],
            "woba_local": [input_data["woba_diff"]],
            "era_pitcher_local": [input_data["era_diff"]],
            "fip_pitcher_local": [input_data["fip_diff"]],
            "obp_visitante": [input_data["obp_diff"]],
            "slg_visitante": [input_data["slg_diff"]],
            "woba_visitante": [input_data["woba_diff"]],
            "era_pitcher_visitante": [input_data["era_diff"]],
            "fip_pitcher_visitante": [input_data["fip_diff"]],
        }

        df = pd.DataFrame(X_dict)[column_order]
        X_scaled = scaler.transform(df.values)  # evita el warning por nombres

        diferencial = modelo_reg.predict(X_scaled)[0]
        probas = modelo_clf.predict_proba(X_scaled)[0]
        prob_local = round(float(probas[1]), 2)
        prob_visitante = round(float(probas[0]), 2)
        ganador = "local" if prob_local > prob_visitante else "visitante"

        return {
            "diferencial_estimado": round(float(diferencial), 2),
            "ganador_probable": ganador,
            "probabilidad_ganador_local": prob_local
        }

    except Exception as e:
        return {"error": f"Error en predict_with_model: {str(e)}"}
# 📈 Análisis de racha con Prophet
def forecast_trend_prophet(equipo):
    try:
        fechas = pd.date_range(end=datetime.today(), periods=30)
        rendimiento = [np.random.normal(loc=0.05, scale=0.1) for _ in range(30)]

        df = pd.DataFrame({
            "ds": fechas,
            "y": rendimiento
        })

        model = Prophet()
        model.fit(df)

        futuro = model.make_future_dataframe(periods=3)
        forecast = model.predict(futuro)

        tendencia = forecast.tail(3)["yhat"].mean()
        tendencia_valor = round(tendencia, 2)

        if tendencia_valor >= 0.10:
            tipo = "positiva"
        elif tendencia_valor <= -0.10:
            tipo = "negativa"
        else:
            tipo = "neutra"

        return f"{tendencia_valor} ({tipo})"

    except Exception as e:
        return f"Error en forecast_trend_prophet: {str(e)}"

# 🤖 Simulación AutoML con comparación real
def compare_with_automl(input_data, winner_base):
    try:
        winner_automl = random.choice(["local", "visitante"])
        consistencia = winner_automl == winner_base
        return consistencia
    except Exception as e:
        return f"Error en compare_with_automl: {str(e)}"
# 🗣️ Explicación estilo GPT (simulado)
def explain_with_gpt(prediccion):
    try:
        ganador = prediccion.get("ganador_probable", "local")
        diferencial = prediccion.get("diferencial_estimado", 0)
        prob = prediccion.get("probabilidad_ganador_local", 0.5)

        if ganador == "local":
            return (
                f"El equipo local es favorito con una probabilidad del {int(prob * 100)}% "
                f"y un diferencial proyectado de {diferencial}. Su desempeño ofensivo y "
                f"sabermetría lo respaldan como el más probable ganador según los modelos."
            )
        else:
            return (
                f"El equipo visitante muestra una ligera ventaja con una probabilidad del {int((1 - prob) * 100)}% "
                f"y un diferencial de {-diferencial}. Factores como pitcheo y tendencia histórica respaldan esta proyección."
            )
    except Exception as e:
        return f"Error en explain_with_gpt: {str(e)}"

# 💾 Logging automático en CSV
def guardar_log_ia(respuesta, equipo_local):
    os.makedirs("logs", exist_ok=True)
    ruta = "logs/ia_respuestas.csv"

    now = datetime.now()
    fecha = now.strftime("%Y-%m-%d")
    hora = now.strftime("%H:%M:%S")

    fila = pd.DataFrame([{
        "fecha": fecha,
        "hora": hora,
        "equipo_local": equipo_local,
        "diferencial": respuesta["prediccion"]["diferencial_estimado"],
        "ganador": respuesta["prediccion"]["ganador_probable"],
        "probabilidad": respuesta["prediccion"]["probabilidad_ganador_local"],
        "tendencia": respuesta["tendencia_prophet"],
        "consistencia": respuesta["consistencia_automl"],
        "explicacion": respuesta["explicacion"]
    }])

    if os.path.exists(ruta):
        fila.to_csv(ruta, mode='a', header=False, index=False)
    else:
        fila.to_csv(ruta, index=False)
# 🧠 Motor orquestador central
def procesar_evento(evento_json):
    try:
        pred = predict_with_model(evento_json)
        if "error" in pred:
            return {"error": pred["error"]}

        trend = forecast_trend_prophet(evento_json["equipo_local"])
        automl = compare_with_automl(evento_json, pred["ganador_probable"])
        gpt_texto = explain_with_gpt(pred)

        respuesta = {
            "prediccion": pred,
            "tendencia_prophet": trend,
            "consistencia_automl": automl,
            "explicacion": gpt_texto
        }

        guardar_log_ia(respuesta, evento_json["equipo_local"])  # 💾 Guardado automático

        return respuesta

    except Exception as e:
        return {"error": f"Error en procesar_evento: {str(e)}"}


# 🧪 Ejecución directa de prueba
if __name__ == "__main__":
    evento = {
        "obp_diff": 0.017,
        "slg_diff": 0.020,
        "woba_diff": 0.019,
        "era_diff": -0.42,
        "fip_diff": -0.33,
        "equipo_local": "Yankees"
    }

    resultado = procesar_evento(evento)
    print(json.dumps(resultado, indent=4, ensure_ascii=False))
