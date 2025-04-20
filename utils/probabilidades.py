import math
import random

def calcular_poisson(media_goles_local, media_goles_visitante, max_goles=5):
    probabilidades = {}
    for gl in range(0, max_goles + 1):
        for gv in range(0, max_goles + 1):
            p1 = (math.exp(-media_goles_local) * media_goles_local**gl) / math.factorial(gl)
            p2 = (math.exp(-media_goles_visitante) * media_goles_visitante**gv) / math.factorial(gv)
            probabilidades[(gl, gv)] = round(p1 * p2, 6)
    return probabilidades

def simular_monte_carlo(prob_local, prob_visitante, simulaciones=10000):
    resultados = {"local_win": 0, "draw": 0, "away_win": 0}
    for _ in range(simulaciones):
        rnd = random.random()
        if rnd < prob_local:
            resultados["local_win"] += 1
        elif rnd < prob_local + prob_visitante:
            resultados["away_win"] += 1
        else:
            resultados["draw"] += 1
    return {
        "local_win": round(resultados["local_win"] / simulaciones, 4),
        "draw": round(resultados["draw"] / simulaciones, 4),
        "away_win": round(resultados["away_win"] / simulaciones, 4)
    }

def generar_kelly(prob_real, cuota):
    b = cuota - 1
    q = 1 - prob_real
    kelly = (b * prob_real - q) / b
    return round(kelly, 4) if kelly > 0 else 0

def valor_esperado(prob_real, cuota):
    ve = (prob_real * cuota) - 1
    return round(ve, 4)
