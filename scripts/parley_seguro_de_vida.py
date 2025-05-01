import json
import sys
import os
from itertools import combinations
from datetime import date
from functools import reduce
from math import prod
import csv
from pathlib import Path

# 🔧 Añadir la ruta del módulo matemático
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'gpt_sanpro')))

# 📥 Importar funciones matemáticas
try:
    from calculo_matematico import (
        calcular_valor_esperado,
        calcular_probabilidad_conjunta
    )
except ImportError:
    print("⚠️ Usando funciones internas de emergencia")
    def calcular_valor_esperado(probabilidad, cuota):
        return round((probabilidad * cuota) - (1 - probabilidad), 3)
    def calcular_probabilidad_conjunta(probabilidades):
        return round(reduce(lambda x, y: x * y, probabilidades), 4)

# ✅ 1. Generar combinaciones válidas
def generar_combinaciones_validas(picks, r=2):
    if len(picks) < r:
        return []
    return list(combinations(picks, r))

# ✅ 2. Calcular métricas del parley
def calcular_parley_metrics(combinacion):
    cuotas = [float(p["cuota"]) for p in combinacion]
    probabilidades = [float(p["probabilidad"]) for p in combinacion]
    eventos = [p["evento"] for p in combinacion]

    cuota_total = round(prod(cuotas), 2)
    prob_total = calcular_probabilidad_conjunta(probabilidades)
    ev_total = calcular_valor_esperado(prob_total, cuota_total)

    return {
        "combinacion": eventos,
        "cuotas": cuotas,
        "cuota_total": cuota_total,
        "probabilidad_total": round(prob_total, 3),
        "valor_esperado": round(ev_total, 3)
    }

# ✅ 3. Clasificar un parley como APTO o RECHAZADO
def clasificar_parley(parley):
    if (
        parley["probabilidad_total"] >= 0.30 and
        parley["valor_esperado"] >= 1.00 and
        parley["cuota_total"] >= 3.5
    ):
        return "APTO"
    return "RECHAZADO"

# ✅ 4. Exportar parleys APTO a JSON
def exportar_parleys_json(lista_final, archivo_salida):
    salida = {
        "fecha": str(date.today()),
        "parleys": lista_final
    }
    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(lista_final)} parleys exportados a {archivo_salida}")

# ✅ 5. Log CSV con todos los parleys
def log_parleys_csv(lista_parleys, archivo_log="logs/parley_log.csv"):
    Path("logs").mkdir(parents=True, exist_ok=True)

    with open(archivo_log, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "fecha", "combinacion", "cuota_total", "probabilidad_total",
            "valor_esperado", "clasificacion"
        ])
        writer.writeheader()

        for parley in lista_parleys:
            writer.writerow({
                "fecha": str(date.today()),
                "combinacion": " | ".join(parley["combinacion"]),
                "cuota_total": parley["cuota_total"],
                "probabilidad_total": parley["probabilidad_total"],
                "valor_esperado": parley["valor_esperado"],
                "clasificacion": parley.get("clasificacion", "N/A")
            })
    print(f"📁 Log guardado en {archivo_log}")

# ✅ 6. Ejecución principal
if __name__ == "__main__":
    try:
        with open("data/picks_validados.json", "r", encoding="utf-8") as f:
            picks = json.load(f)

        picks = [p for p in picks if p.get("estado") == "APTO"]

        if len(picks) < 2:
            print("⚠️ No hay suficientes picks APTO para combinar.")
            exit()

        resultados = []

        for r in [2, 3]:
            combinaciones = generar_combinaciones_validas(picks, r)
            for combo in combinaciones:
                parley = calcular_parley_metrics(combo)
                parley["clasificacion"] = clasificar_parley(parley)
                resultados.append(parley)

        # 📝 Log de todos los parleys
        log_parleys_csv(resultados)

        # 💾 Exportar solo los APTO
        exportar_parleys_json(
            [p for p in resultados if p["clasificacion"] == "APTO"],
            "data/parleys_generados.json"
        )

    except Exception as e:
        print(f"❌ Error general: {str(e)}")
