from flask import Flask, request, render_template, send_from_directory, jsonify 
from utils import probabilidades
from predictor import predecir_resultado
from dotenv import load_dotenv
load_dotenv()
from utils.baseball_predictor import predecir_super_altas_bajas
from datetime import datetime
import hashlib


app = Flask(__name__)

@app.route("/super_altas_bajas", methods=["GET"])
def prediccion_over_under():
    equipo1 = request.args.get("equipo1")
    equipo2 = request.args.get("equipo2")

    # Ejemplo temporal — luego se conecta a la base o API de enfrentamientos reales
    partidos = [
        {"carreras_local": 6, "carreras_visita": 4},
        {"carreras_local": 5, "carreras_visita": 3},
        {"carreras_local": 8, "carreras_visita": 2}
    ]

    from utils.baseball_predictor import predecir_super_altas_bajas
    resultado = predecir_super_altas_bajas(partidos)

    # 🔐 Código de verificación único SAMPRO
    now = datetime.utcnow().isoformat()
    base = f"{equipo1}-{equipo2}-{resultado['over_under']}-{now}"
    codigo_sampro = hashlib.sha256(base.encode()).hexdigest()[:12].upper()

    resultado.update({
        "equipo1": equipo1,
        "equipo2": equipo2,
        "fecha": now,
        "codigo_sampro": codigo_sampro
    })

    return jsonify(resultado)


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
    if "apostar ahora" in texto or "apostar en" in texto:
        from utils.apis.cuotas import obtener_cuotas
        from utils.apis.fixtures import buscar_fixture_con_cuotas
        from banca import registrar_apuesta
        from predictor import predecir_resultado

        try:
            if "apostar ahora" in texto:
                partido = buscar_fixture_con_cuotas()
                if "error" in partido:
                    respuesta = f"❌ No se encontraron partidos con cuotas: {partido['error']}"
                else:
                    fixture_id = partido["fixture_id"]
                    equipo_local = partido["local"]
                    equipo_visitante = partido["visitante"]
            else:
                fixture_id = int(texto.split("apostar en")[1].strip())
                equipo_local = "Equipo Local"
                equipo_visitante = "Equipo Visitante"

                cuota_info = obtener_cuotas(fixture_id)
                if "error" in cuota_info:
                    respuesta = f"❌ Error al obtener cuotas: {cuota_info['error']}"
                else:
                    goles_local = 1.6
                    goles_visita = 1.2
                    resultado = predecir_resultado(goles_local, goles_visita)
                    probabilidad = resultado["probabilidad_gana_local"]
                    cuota = cuota_info["local"]

                    # ❗ Esto es temporal. Luego se reemplaza con el resultado real del fixture
        except Exception as e:
            respuesta = f"❌ Error al procesar la solicitud: {str(e)}"
        from utils.apis.resultados import resultado_real
        resultado = resultado_real(fixture_id)
        if "error" in resultado:
            acertado = probabilidad > 0.5  # fallback
        else:
            acertado = resultado["acertado"]
           
            banca_res = registrar_apuesta(fixture_id, probabilidad, cuota, acertado)

            respuesta = f"""
            🧠 <b>Apuesta Inteligente</b><br>
            ⚔️ {equipo_local} vs {equipo_visitante}<br>
            🎯 Predicción: {round(probabilidad * 100, 2)}%<br>
            💸 Cuota usada: {cuota}<br>
            🧾 Resultado: {"✔️ GANÓ" if acertado else "❌ PERDIÓ"}<br>
            💰 {banca_res}
            """
        # Removed misplaced except block

    elif "estadisticas de" in texto:
        from utils.apis.estadisticas import obtener_estadisticas
        try:
            partes = texto.replace("estadisticas de", "").strip().split("equipo")
            fixture_id = int(partes[0].strip())
            team_id = int(partes[1].strip())
            stats = obtener_estadisticas(fixture_id, team_id)

            if isinstance(stats, dict) and "error" in stats:
                respuesta = f"❌ Error: {stats['error']}"
            else:
                respuesta = f"📊 <b>Estadísticas del equipo {team_id} en el partido {fixture_id}:</b><br>"
                for linea in stats:
                    respuesta += f"• {linea}<br>"

        except Exception as e:
            respuesta = f"❌ Error procesando IDs: {str(e)}"

    elif "cuotas en" in texto:
            from utils.apis.cuotas import obtener_cuotas
            try:
                fixture_id = int(texto.split("cuotas en")[1].strip())
                cuotas = obtener_cuotas(fixture_id)

                if "error" in cuotas:
                    respuesta = f"❌ Error: {cuotas['error']}"
                else:
                    respuesta = f"""
                    💰 <b>Cuotas para el partido {fixture_id}</b><br>
                    🏦 Casa: {cuotas['casa']}<br>
                    🟢 Gana local: {cuotas['local']}<br>
                    ⚪ Empate: {cuotas['empate']}<br>
                    🔴 Gana visitante: {cuotas['visitante']}
                    """
            except Exception as e:
                respuesta = f"❌ Error procesando el fixture ID: {str(e)}"

    elif "eventos en" in texto:
            from utils.apis.eventos import obtener_eventos
            try:
                fixture_id = int(texto.split("eventos en")[1].strip())
                eventos = obtener_eventos(fixture_id)
    
                if "error" in eventos:
                    respuesta = f"❌ Error: {eventos['error']}"
                else:
                    respuesta = f"📺 <b>Eventos del partido {fixture_id}:</b><br>"
                    for e in eventos["response"]:
                        tipo = e["type"]
                        detalle = e["detail"]
                        jugador = e["player"]["name"]
                        equipo = e["team"]["name"]
                        minuto = e["time"]["elapsed"]
                        respuesta += f"⏱️ {minuto}’ - {jugador} ({equipo}) → {tipo} ({detalle})<br>"
    
            except Exception as e:
                respuesta = f"❌ Error procesando el fixture ID: {str(e)}"

    elif "racha de bayern" in texto:
            from utils.rachas import obtener_racha
            racha = obtener_racha(team_id=157)
    
            if "error" in racha:
                respuesta = f"❌ Error al obtener la racha: {racha['error']}"
            else:
                respuesta = "📊 <b>Últimos 5 partidos del Bayern:</b><br>"
                for linea in racha["racha"]:
                    respuesta += f"• {linea}<br>"
                respuesta += f"<br>⚽ Goles marcados: {racha['goles_marcados']}<br>🛡️ Goles recibidos: {racha['goles_recibidos']}<br>📈 {racha['resumen']}"

    elif "lesiones en bayern" in texto:
            from utils.lesiones import obtener_lesiones
            jugadores_lesionados = obtener_lesiones(team_id=157)
            respuesta = "🩼 <b>Jugadores lesionados en Bayern:</b><br>"
            for j in jugadores_lesionados:
                respuesta += f"• {j}<br>"
    
    elif "clima en" in texto:
            from utils.clima import obtener_clima
            lat = 4.6097
            lon = -74.0817
            clima = obtener_clima(lat, lon)
    
            if "error" in clima:
                respuesta = f"❌ Error obteniendo el clima: {clima['error']}"
            else:
                respuesta = f"""
                ☁️ <b>Clima en Bogotá</b><br>
                🌡️ Temp: {clima['temperatura']} °C<br>
                💧 Humedad: {clima['humedad']}%<br>
                🌬️ Viento: {clima['viento']} m/s<br>
                🌥️ Condición: {clima['condicion']}
                """

    else:
            respuesta = "❌ Comando no reconocido"

    return render_template('index.html', response=respuesta)

@app.route("/super_altas_bajas", methods=["GET"])
def prediccion_over_under():
    equipo1 = request.args.get("equipo1")
    equipo2 = request.args.get("equipo2")

    partidos = [
        {"carreras_local": 6, "carreras_visita": 4},
        {"carreras_local": 5, "carreras_visita": 3},
        {"carreras_local": 8, "carreras_visita": 2}
    ]

    resultado = predecir_super_altas_bajas(partidos)

    now = datetime.utcnow().isoformat()
    base = f"{equipo1}-{equipo2}-{resultado['over_under']}-{now}"
    codigo_sampro = hashlib.sha256(base.encode()).hexdigest()[:12].upper()

    resultado.update({
        "equipo1": equipo1,
        "equipo2": equipo2,
        "fecha": now,
        "codigo_sampro": codigo_sampro
    })

    return jsonify(resultado)


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
