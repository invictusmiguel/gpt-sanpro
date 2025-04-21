import os
import json
from datetime import datetime
from banca import registrar_apuesta
from predictor import predecir_resultado

# Ruta donde están los partidos recolectados hoy
DATA_DIR = "data_diaria"
FECHA_HOY = datetime.today().strftime("%Y-%m-%d")

# Buscar archivos .json de hoy
partidos = [f for f in os.listdir(DATA_DIR) if f.startswith(FECHA_HOY) and f.endswith(".json")]

if not partidos:
    print("❌ No hay partidos con cuotas disponibles hoy.")
    exit()

# Seleccionar el primero disponible
archivo = partidos[0]
ruta = os.path.join(DATA_DIR, archivo)

with open(ruta, "r", encoding="utf-8") as f:
    datos = json.load(f)

# Leer info
fixture_id = int(archivo.split("_")[1])
equipo_local = archivo.split("_")[2]
equipo_visitante = archivo.split("_")[-1].replace(".json", "")

# Extraer cuota
try:
    cuota_local = float(datos["response"][0]["bookmakers"][0]["bets"][0]["values"][0]["odd"])
except:
    print("❌ Error extrayendo cuota del archivo")
    exit()

# Simular promedio de goles
goles_local = 1.6
goles_visita = 1.2
resultado = predecir_resultado(goles_local, goles_visita)
probabilidad = resultado["probabilidad_gana_local"]
acertado = probabilidad > 0.5

# Ejecutar apuesta
banca = registrar_apuesta(fixture_id, probabilidad, cuota_local, acertado)

# Mostrar resultado
print(f"""
📊 Apuesta Inteligente Ejecutada
🆚 {equipo_local} vs {equipo_visitante}
🎯 Probabilidad estimada: {round(probabilidad * 100, 2)}%
💸 Cuota: {cuota_local}
🧾 Resultado: {"✔️ GANÓ" if acertado else "❌ PERDIÓ"}
💰 {banca}
""")
