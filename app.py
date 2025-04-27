from flask import Flask, request, render_template, send_from_directory, jsonify
from dotenv import load_dotenv
import os
import json
import hashlib
from datetime import datetime, timezone

# Carga variables de entorno
load_dotenv()
# 📦 Importaciones necesarias
import joblib
import numpy as np
from flask import Flask, request, jsonify

# 🔵 Cargar modelos y scaler entrenados
try:
    scaler = joblib.load('models/scaler.pkl')
    print("✅ Scaler cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar scaler: {e}")

try:
    modelo_regresion = joblib.load('models/regression_model.pkl')
    print("✅ Modelo de regresión cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar modelo de regresión: {e}")

try:
    modelo_clasificacion = joblib.load('models/classification_model.pkl')
    print("✅ Modelo de clasificación cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar modelo de clasificación: {e}")

# 🔵 Inicializar Flask
app = Flask(__name__)

# 📦 Importaciones del proyecto
from utils import probabilidades
from predictor import predecir_resultado
from utils.baseball_predictor import predecir_super_altas_bajas
from utils.parleys.parley_seguro_vida import generar_parleys_seguro_vida

# Inicializa Flask
app = Flask(__name__)

# -----------------------------------
# 📦 Cargar Scaler y Modelos de Machine Learning
# -----------------------------------
import joblib
import numpy as np

# Cargar el scaler
try:
    scaler = joblib.load('models/scaler.pkl')
    print("✅ Scaler cargado correctamente.")
except Exception as e:
    print(f"❌ Error cargando scaler.pkl: {str(e)}")

# Cargar el modelo de regresión (diferencial de carreras)
try:
    modelo_regresion = joblib.load('models/modelo_regresion.pkl')
    print("✅ Modelo de regresión cargado correctamente.")
except Exception as e:
    print(f"❌ Error cargando modelo_regresion.pkl: {str(e)}")

# Cargar el modelo de clasificación (probabilidad de victoria)
try:
    modelo_clasificacion = joblib.load('models/modelo_clasificacion.pkl')
    print("✅ Modelo de clasificación cargado correctamente.")
except Exception as e:
    print(f"❌ Error cargando modelo_clasificacion.pkl: {str(e)}")

# 🧠 Ruta principal HTML para comandos desde el navegador
@app.route("/", methods=["GET", "POST"])
def index():
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

        elif "parley" in texto:
            try:
                with open("data/cuotas_diarias.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    picks = data["partidos"]

                parlays = generar_parleys_seguro_vida(picks)

                if isinstance(parlays, list) and "error" in parlays[0]:
                    respuesta = f"⚠️ {parlays[0]['error']}"
                else:
                    respuesta = "<h2>💼 Estrategia Seguro de Vida (SAMPRO)</h2>"
                    for parley in parlays:
                        respuesta += f"<h3>🎯 {parley['nombre']}</h3>"
                        respuesta += f"<b>Cuota Total:</b> {parley['cuota_total']}<br>"
                        respuesta += f"<b>Probabilidad:</b> {round(parley['probabilidad'] * 100, 2)}%<br>"
                        respuesta += f"<b>Valor Esperado:</b> {parley['valor_esperado']}<br>"
                        respuesta += f"<b>Inversión:</b> {parley['inversion']} soles<br>"
                        respuesta += f"<b>Código SAMPRO:</b> {parley['codigo_sampro']}<br><ul>"
                        for pick in parley["picks"]:
                            respuesta += f"<li>{pick['partido']} — {pick['mercado']} — Cuota: {pick['cuota']} — Confianza: {pick['confianza']}%</li>"
                        respuesta += "</ul><hr>"

            except Exception as e:
                respuesta = f"❌ Error generando parley: {str(e)}"

        else:
            respuesta = "❌ Comando no reconocido"

    return render_template("index.html", response=respuesta)
# --------------------------------------------------
# 📊 Endpoint para predicción de over/under
# --------------------------------------------------

@app.route("/super_altas_bajas", methods=["GET"])
def prediccion_over_under():
    equipo1 = request.args.get("equipo1")
    equipo2 = request.args.get("equipo2")

    # 🔄 Simulación de partidos históricos
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
# -----------------------------------
# 🎯 Endpoint de Predicción Oficial /predict
# -----------------------------------
# 🎯 Endpoint de Predicción Oficial /predict (Mejorado con validaciones)
# 🔵 Endpoint para hacer predicciones
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Validar campos obligatorios
        required_fields = ['obp_diff', 'slg_diff', 'woba_diff', 'era_diff', 'fip_diff']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Falta el campo obligatorio: {field}'}), 400

        # Crear el vector de entrada
        input_data = np.array([
            data['obp_diff'],
            data['slg_diff'],
            data['woba_diff'],
            data['era_diff'],
            data['fip_diff']
        ]).reshape(1, -1)

        # Como nuestros modelos esperan 10 features (local y visitante por separado),
        # duplicamos los diferenciales para completar
        input_data_full = np.hstack((input_data, input_data))  # Ahora son 10 columnas

        # Escalar los datos
        input_scaled = scaler.transform(input_data_full)

        # Hacer predicciones
        diferencial_predicho = modelo_regresion.predict(input_scaled)[0]
        probas = modelo_clasificacion.predict_proba(input_scaled)[0]
        prob_local = round(float(probas[1]), 2)
        prob_visitante = round(float(probas[0]), 2)
        equipo_ganador = "local" if prob_local > prob_visitante else "visitante"

        # Devolver respuesta
        return jsonify({
            'diferencial_carreras_estimado': round(float(diferencial_predicho), 2),
            'equipo_ganador_probable': equipo_ganador,
            'probabilidad_ganador_local': prob_local,
            'probabilidad_ganador_visitante': prob_visitante
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --------------------------------------------------
# 🧠 Endpoint para predicción de probabilidades básicas
# --------------------------------------------------

@app.route('/prediccion', methods=['GET'])
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

# --------------------------------------------------
# 🌐 Plugins de manifest y logo
# --------------------------------------------------

@app.route('/.well-known/ai-plugin.json')
def serve_manifest():
    return send_from_directory('.well-known', 'ai-plugin.json', mimetype='application/json')

@app.route('/openapi.yaml')
def serve_openapi():
    return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')

@app.route('/static/logo.png')
def serve_logo():
    return send_from_directory('static', 'logo.png', mimetype='image/png')
# --------------------------------------------------
# 💼 Endpoint para Parley Seguro de Vida (HTML)
# --------------------------------------------------

@app.route("/parley_seguro_vida", methods=["GET"])
def parley_seguro_vida():
    try:
        with open("data/cuotas_diarias.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            picks = data["partidos"]
    except Exception as e:
        return f"❌ Error al cargar datos: {str(e)}"

    parlays = generar_parleys_seguro_vida(picks)

    if isinstance(parlays[0], dict) and "error" in parlays[0]:
        return f"<h3>⚠️ {parlays[0]['error']}</h3>"

    respuesta = "<h2>💼 Estrategia Seguro de Vida (SAMPRO v1.8.1)</h2>"

    for parley in parlays:
        respuesta += f"<h3>🎯 {parley['nombre']}</h3>"
        respuesta += f"<b>Cuota Total:</b> {parley['cuota_total']}<br>"
        respuesta += f"<b>Probabilidad:</b> {round(parley['probabilidad'] * 100, 2)}%<br>"
        respuesta += f"<b>Valor Esperado:</b> {parley['valor_esperado']}<br>"
        respuesta += f"<b>Inversión:</b> {parley['inversion']} soles<br>"
        respuesta += f"<b>Código SAMPRO:</b> {parley['codigo_sampro']}<br><ul>"

        for pick in parley["picks"]:
            respuesta += f"<li>{pick['partido']} — {pick['mercado']} — Cuota: {pick['cuota']} — Confianza: {pick['confianza']}%</li>"
        respuesta += "</ul><hr>"

    return respuesta

# --------------------------------------------------
# 🧾 Versión JSON del endpoint Parley Seguro de Vida
# --------------------------------------------------

@app.route("/parley_seguro_vida_json", methods=["GET"])
def parley_seguro_vida_json():
    try:
        with open("data/cuotas_diarias.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
            picks = datos.get("partidos", [])
    except Exception as e:
        return {"error": f"No se pudo leer cuotas_diarias.json: {str(e)}"}, 500

    parlays = generar_parleys_seguro_vida(picks)

    if isinstance(parlays, list) and "error" in parlays[0]:
        return {"error": parlays[0]["error"]}, 200

    return {"parleys": parlays}, 200

# --------------------------------------------------
# 🟢 Iniciar servidor Flask
# --------------------------------------------------

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
