# utils/probabilidades.py

import math
import random

def calcular_poisson(media_local, media_visitante, max_goles=5):
    """
    Calcula las probabilidades de todos los marcadores posibles usando distribución de Poisson.
    Devuelve un diccionario con claves (goles_local, goles_visitante): probabilidad
    """
    probabilidades = {}
    for gl in range(0, max_goles + 1):
        for gv in range(0, max_goles + 1):
            p1 = (math.exp(-media_local) * media_local**gl) / math.factorial(gl)
            p2 = (math.exp(-media_visitante) * media_visitante**gv) / math.factorial(gv)
            probabilidades[(gl, gv)] = round(p1 * p2, 6)
    return probabilidades

def simular_monte_carlo(prob_local, prob_visitante, simulaciones=10000):
    """
    Simula partidos según probabilidades dadas.
    Retorna proporciones de victorias locales, empates y visitantes.
    """
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
    """
    Calcula el porcentaje de bankroll ideal según el criterio de Kelly.
    Si el resultado es negativo, se devuelve 0.
    """
    b = cuota - 1
    q = 1 - prob_real
    kelly = (b * prob_real - q) / b
    return round(kelly, 4) if kelly > 0 else 0

def valor_esperado(prob_real, cuota):
    """
    Determina si una apuesta tiene valor esperado positivo.
    Retorna un número: si es mayor a 0, hay valor.
    """
    ve = (prob_real * cuota) - 1
    return round(ve, 4)
