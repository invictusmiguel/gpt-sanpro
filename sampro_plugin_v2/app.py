# 📦 Importaciones necesarias
from flask import Flask, request, render_template, send_from_directory, jsonify
from dotenv import load_dotenv
import os
import json
import hashlib
from datetime import datetime, timezone
import joblib
import numpy as np
import pandas as pd  # 📚 Importante: pandas se usa en /predict

# 📦 Importaciones internas del proyecto
from utils import probabilidades
from predictor import predecir_resultado
from utils.baseball_predictor import predecir_super_altas_bajas
from routes.parley_seguro_vida import bp as parley_seguro_vida_bp  # ✅ INTEGRACIÓN DEL BOT

# 🔵 Cargar variables de entorno (.env)
load_dotenv()

# 🔵 Inicializar la app Flask
app = Flask(__name__)
app.register_blueprint(parley_seguro_vida_bp)  # ✅ REGISTRO DEL BLUEPRINT

# 🔵 Cargar Scaler y Modelos entrenados
try:
    scaler = joblib.load('models/scaler.pkl')
    print("✅ Scaler cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar el scaler: {e}")

try:
    modelo_regresion = joblib.load('models/regression_model.pkl')
    print("✅ Modelo de regresión cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar el modelo de regresión: {e}")

try:
    modelo_clasificacion = joblib.load('models/classification_model.pkl')
    print("✅ Modelo de clasificación cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar el modelo de clasificación: {e}")
# 🧠 Ruta principal - Página de inicio
@app.route("/", methods=["GET", "POST"])
def inicio():
    respuesta = ""

    if request.method == "POST":
        texto = request.form.get("comando", "").lower()

        if "modo experto on" in texto:
            goles_local = 1.8
            goles_visitante = 1.2
            cuota = 2.1
            prob_real = 0.55

            poisson = probabilidades.calcular_poisson(goles_local, goles_visitante)
            simulacion = probabilidades.simular_monte_carlo(prob_real, 1 - prob_real)
            kelly = probabilidades.generar_kelly(prob_real, cuota)
            ve = probabilidades.valor_esperado(prob_real, cuota)

            respuesta = f"""
            🔓 <b>Modo Experto Activado</b><br>
            ✔️ Poisson: {goles_local}-{goles_visitante}<br>
            ✔️ Monte Carlo: {simulacion}<br>
            ✔️ Kelly: {kelly * 100:.2f}%<br>
            ✔️ Valor Esperado: {ve}
            """
        
        else:
            respuesta = "❌ Comando no reconocido"

    return render_template("index.html", response=respuesta)
# 🎯 Endpoint de predicción oficial /predict
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        required_fields = ['obp_diff', 'slg_diff', 'woba_diff', 'era_diff', 'fip_diff']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Falta el campo obligatorio: {field}'}), 400

        # Armar el dataframe para la predicción
        input_dict = {
            "obp_local": [data['obp_diff']],
            "slg_local": [data['slg_diff']],
            "woba_local": [data['woba_diff']],
            "era_pitcher_local": [data['era_diff']],
            "fip_pitcher_local": [data['fip_diff']],
            "obp_visitante": [data['obp_diff']],
            "slg_visitante": [data['slg_diff']],
            "woba_visitante": [data['woba_diff']],
            "era_pitcher_visitante": [data['era_diff']],
            "fip_pitcher_visitante": [data['fip_diff']],
        }

        input_data_full = pd.DataFrame(input_dict)

        # Escalar los datos
        input_scaled = scaler.transform(input_data_full)

        # Predicciones
        diferencial_predicho = modelo_regresion.predict(input_scaled)[0]
        probas = modelo_clasificacion.predict_proba(input_scaled)[0]
        prob_local = round(float(probas[1]), 2)
        prob_visitante = round(float(probas[0]), 2)
        equipo_ganador = "local" if prob_local > prob_visitante else "visitante"

        return jsonify({
            'diferencial_carreras_estimado': round(float(diferencial_predicho), 2),
            'equipo_ganador_probable': equipo_ganador,
            'probabilidad_ganador_local': prob_local,
            'probabilidad_ganador_visitante': prob_visitante
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 📊 Endpoint de predicción Over/Under (Altas/Bajas)
@app.route("/super_altas_bajas", methods=["GET"])
def prediccion_over_under():
    equipo1 = request.args.get("equipo1")
    equipo2 = request.args.get("equipo2")

    # Datos de ejemplo para simular partidos
    partidos = [
        {"carreras_local": 6, "carreras_visita": 4},
        {"carreras_local": 5, "carreras_visita": 3},
        {"carreras_local": 8, "carreras_visita": 2}
    ]

    resultado = predecir_super_altas_bajas(partidos)

    now = datetime.now(timezone.utc).isoformat()
    base = f"{equipo1}-{equipo2}-{resultado['over_under']}-{now}"
    codigo_sampro = hashlib.sha256(base.encode()).hexdigest()[:12].upper()

    resultado.update({
        "equipo1": equipo1,
        "equipo2": equipo2,
        "fecha": now,
        "codigo_sampro": codigo_sampro
    })

    return jsonify(resultado)
# 🧠 Endpoint básico de probabilidades de goles
@app.route("/prediccion", methods=["GET"])
def prediccion_api():
    try:
        gl = float(request.args.get('goles_local', 0))
        gv = float(request.args.get('goles_visita', 0))
        resultado = predecir_resultado(gl, gv)
        return {
            "probabilidad_local": resultado['probabilidad_gana_local'],
            "probabilidad_no_local": resultado['probabilidad_no_gana_local']
        }
    except Exception as e:
        return {"error": str(e)}, 400


# 🌐 Endpoint para servir el manifest del plugin (ai-plugin.json)
@app.route("/.well-known/ai-plugin.json", methods=["GET"])
def serve_plugin_manifest():
    try:
        return send_from_directory(".well-known", "ai-plugin.json", mimetype="application/json")
    except Exception as e:
        return jsonify({"error": f"No se pudo servir ai-plugin.json: {str(e)}"}), 500


# 🌐 Endpoint para servir el archivo OpenAPI (openapi.yaml)
@app.route("/openapi.yaml", methods=["GET"])
def serve_openapi():
    try:
        return send_from_directory(".", "openapi.yaml", mimetype="text/yaml")
    except Exception as e:
        return jsonify({"error": f"No se pudo servir openapi.yaml: {str(e)}"}), 500


# 🌐 Endpoint para servir el logo del plugin
@app.route("/static/logo.png", methods=["GET"])
def serve_logo():
    try:
        return send_from_directory("static", "logo.png", mimetype="image/png")
    except Exception as e:
        return jsonify({"error": f"No se pudo servir logo.png: {str(e)}"}), 500
# ❌ Manejo elegante de errores 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("index.html", response="❌ Página no encontrada."), 404


# 🚀 Lanzar el servidor Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Carga el puerto de .env o usa 5000
    app.run(host="0.0.0.0", port=port, debug=True)  # debug=True solo en desarrollo
