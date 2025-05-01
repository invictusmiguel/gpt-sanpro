import json
import random
import csv
from datetime import datetime
from pathlib import Path

# ⚾ Equipos ficticios (puedes reemplazarlos con lectura desde cuotas_mlbbulk.json)
EQUIPOS_MLB = [
    "Yankees", "Red Sox", "Dodgers", "Braves", "Mets", "Cubs",
    "Giants", "Cardinals", "Astros", "Rays"
]

# 🧠 Nombres simulados
PITCHERS = ["Gerrit Cole", "Max Scherzer", "Jacob deGrom", "Shohei Ohtani", "Clayton Kershaw"]
LESIONADOS = ["Judge", "Trout", "Altuve", "Harper", "Betts", None]

# 🎯 Niveles de riesgo
RIESGOS = ["bajo", "medio", "alto"]

# 🔧 Función principal
def generar_boletin_simulado():
    boletin = {}

    for equipo in EQUIPOS_MLB:
        pitcher = random.choice(PITCHERS)
        lesionado = random.choice(LESIONADOS)
        riesgo = random.choice(RIESGOS)

        boletin[equipo] = {
            "pitcher": pitcher,
            "lesionados": [lesionado] if lesionado else [],
            "riesgo": riesgo
        }

    # 📁 Guardar boletín
    Path("data").mkdir(exist_ok=True)
    with open("data/boletin_diario.json", "w", encoding="utf-8") as f:
        json.dump(boletin, f, ensure_ascii=False, indent=2)

    # 📝 Log
    Path("logs").mkdir(exist_ok=True)
    with open("logs/boletin_log.csv", "a", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([now, len(boletin), "OK"])

    print(f"✅ Boletín diario generado para {len(boletin)} equipos en data/boletin_diario.json")

# 🚀 Ejecutar
if __name__ == "__main__":
    generar_boletin_simulado()
