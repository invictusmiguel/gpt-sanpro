import json
import random
import csv
from datetime import datetime
from pathlib import Path

# 🌦️ Climas simulados posibles
CLIMAS_POSIBLES = ["Soleado", "Nublado", "Lluvia leve", "Ventoso", "Despejado"]

# 🧠 Función para simular clima aleatorio
def simular_clima():
    return random.choice(CLIMAS_POSIBLES)

# 🛠️ Función principal
def agregar_clima_a_partidos():
    try:
        # 📂 Leer cuotas MLB reales (cuotas_mlbbulk.json)
        with open("data/cuotas_mlbbulk.json", "r", encoding="utf-8") as f:
            partidos = json.load(f)

        partidos_con_clima = []

        for partido in partidos:
            partido["clima"] = simular_clima()
            partidos_con_clima.append(partido)

        # 💾 Guardar archivo actualizado con clima
        with open("data/cuotas_mlbbulk.json", "w", encoding="utf-8") as f:
            json.dump(partidos_con_clima, f, ensure_ascii=False, indent=2)

        # 📝 Registrar en log
        Path("logs").mkdir(exist_ok=True)
        with open("logs/clima_log.csv", "a", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([now, len(partidos_con_clima), "Clima simulado OK"])

        print(f"✅ Clima simulado agregado a {len(partidos_con_clima)} partidos.")

    except Exception as e:
        print(f"❌ Error procesando clima: {str(e)}")

# 🚀 Ejecutar
if __name__ == "__main__":
    agregar_clima_a_partidos()
