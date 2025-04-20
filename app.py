from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# Cargar claves del archivo .env
load_dotenv()

# Importar módulos utilitarios
from utils.api_football import obtener_partidos_hoy
from utils.logic import generar_parley, calcular_valor
from utils.expert_mode import simular_apuestas

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comando', methods=['POST'])
def comando():
    texto = request.form['comando'].lower()

    if "parley" in texto:
        partidos = obtener_partidos_hoy()
        return generar_parley(partidos)

    elif "valor" in texto:
        return calcular_valor()

    elif "modo experto" in texto and "on" in texto:
        return "🔓 Modo Experto Activado: Simulaciones avanzadas activadas"

    elif "modo experto" in texto and "off" in texto:
        return "🔒 Modo Experto Desactivado"

    elif "simula" in texto or "10.000" in texto:
        return simular_apuestas()

    else:
        return "Comando no reconocido. Intenta con: 'dame un parley', 'valor', 'modo experto ON'."

if __name__ == '__main__':
    # Corrección para Render: puerto dinámico y host 0.0.0.0
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
