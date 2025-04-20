from flask import Flask, request, render_template, send_from_directory 
from utils import probabilidades
from predictor import predecir_resultado

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    respuesta = ""

    if request.method == 'POST':
        texto = request.form.get('comando', '').lower()

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
            ✔️ Poisson {goles_local}-{goles_visitante}<br>
            ✔️ Monte Carlo: {simulacion}<br>
            ✔️ Kelly: {kelly * 100}%<br>
            ✔️ Valor Esperado: {ve}
            """

        elif "predecir" in texto:
            resultado = predecir_resultado(2, 1)
            respuesta = f"""
            🤖 <b>Predicción usando modelo:</b><br>
            ✔️ Probabilidad de que gane el LOCAL: {resultado['probabilidad_gana_local'] * 100}%<br>
            ❌ Probabilidad de que NO gane el LOCAL: {resultado['probabilidad_no_gana_local'] * 100}%
            """

        else:
            respuesta = "❌ Comando no reconocido"

    return render_template('index.html', response=respuesta)

# ----------- API para plugin GPT-SANPRO -----------

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

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
