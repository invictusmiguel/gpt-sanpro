import os
import time

print("🔁 Ejecutando pipeline automático de apuestas deportivas...\n")

# 1. Recolector
print("📥 Recolectando partidos y cuotas reales...")
os.system("python recolector_diario.py")
time.sleep(2)

# 2. Entrenamiento del modelo
print("\n🧠 Entrenando modelo si hay datos nuevos...")
os.system("python entrenamiento.py")
time.sleep(2)

# 3. Auto-apuesta
print("\n🎯 Ejecutando apuesta inteligente...")
os.system("python auto_apuestas.py")
