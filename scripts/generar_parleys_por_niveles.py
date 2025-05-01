import sys
import os
import json
from itertools import combinations
from datetime import date

sys.path.append(os.path.abspath("src"))
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../calculos"))

from gpt_sanpro.calculo_matematico import (
    calcular_valor_esperado,
    calcular_probabilidad_conjunta,
    calcular_kelly,
    calcular_z_score
)

def cargar_picks_validos(ruta="data/picks_validados.json"):
    if not os.path.exists(ruta):
        print(f"⚠️ Archivo no encontrado: {ruta}")
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def nivel_1_combinaciones(picks):
    return generar_parleys(picks)

def nivel_2_combinaciones(picks):
    recomendables = []
    for p in picks:
        ev = calcular_valor_esperado(p["probabilidad"], p["cuota"])
        if p["probabilidad"] >= 0.65 and ev >= 0.80:
            p_copy = p.copy()
            p_copy["ev"] = round(ev, 3)
            recomendables.append(p_copy)
    return generar_parleys(recomendables)

def nivel_3_combinaciones(picks):
    ultra_seguro = []
    for p in picks:
        ev = calcular_valor_esperado(p["probabilidad"], p["cuota"])
        z = calcular_z_score(p.get("cuota", 1.5), 1.65, 0.25)  # media y desviación dummy
        if p["probabilidad"] >= 0.75 and ev >= 1.0 and abs(z) <= 1:
            p_copy = p.copy()
            p_copy["ev"] = round(ev, 3)
            p_copy["z_score"] = z
            ultra_seguro.append(p_copy)
    return generar_parleys(ultra_seguro)

def generar_parleys(lista_picks):
    resultados = []
    for r in [2, 3]:  # parleys de 2 y 3 combinaciones
        combinaciones_r = list(combinations(lista_picks, r))
        for combo in combinaciones_r:
            eventos = [p["evento"] for p in combo]
            cuotas = [p["cuota"] for p in combo]
            probs = [p["probabilidad"] for p in combo]

            cuota_total = round(prod(cuotas), 2)
            prob_total = round(calcular_probabilidad_conjunta(probs), 3)
            ev_total = round(calcular_valor_esperado(prob_total, cuota_total), 2)

            resultados.append({
                "combinacion": eventos,
                "cuotas": cuotas,
                "cuota_total": cuota_total,
                "probabilidad_total": prob_total,
                "valor_esperado": ev_total
            })
    return resultados

def prod(lista):
    resultado = 1
    for num in lista:
        resultado *= num
    return resultado

def exportar_parleys_por_nivel(resultados, ruta="data/parleys_por_nivel.json"):
    os.makedirs("data", exist_ok=True)
    salida = {
        "fecha": str(date.today()),
        "nivel_1": resultados.get("nivel_1", []),
        "nivel_2": resultados.get("nivel_2", []),
        "nivel_3": resultados.get("nivel_3", [])
    }
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(salida, f, indent=2, ensure_ascii=False)
    print(f"[OK] Parleys por nivel exportados a {ruta}")

if __name__ == "__main__":
    print(">> Generando parleys por niveles...")

    picks = cargar_picks_validos()

    if not picks:
        print("⚠️ No hay picks válidos en data/picks_validados.json")
        exit()

    for pick in picks:
        if "ev" not in pick:
            pick["ev"] = round(calcular_valor_esperado(pick["probabilidad"], pick["cuota"]), 3)

    resultados = {
        "nivel_1": nivel_1_combinaciones(picks),
        "nivel_2": nivel_2_combinaciones(picks),
        "nivel_3": nivel_3_combinaciones(picks)
    }

    exportar_parleys_por_nivel(resultados)
