# ✅ 1. Calcular Valor Esperado
def calcular_valor_esperado(probabilidad, cuota):
    """
    Calcula el valor esperado de una apuesta.

    Args:
        probabilidad (float): Probabilidad estimada del evento (ej. 0.70)
        cuota (float): Cuota decimal ofrecida (ej. 1.90)

    Returns:
        float: valor esperado redondeado a 3 decimales
    """
    ev = (probabilidad * cuota) - (1 - probabilidad)
    return round(ev, 3)
# ✅ 2. Calcular probabilidad conjunta
from functools import reduce

def calcular_probabilidad_conjunta(lista_probabilidades):
    """
    Calcula la probabilidad conjunta de una lista de eventos independientes.

    Args:
        lista_probabilidades (list[float]): Lista de probabilidades individuales (ej. [0.75, 0.65, 0.70])

    Returns:
        float: probabilidad conjunta redondeada a 4 decimales
    """
    if not lista_probabilidades:
        return 0.0
    producto = reduce(lambda x, y: x * y, lista_probabilidades)
    return round(producto, 4)
# ✅ 3. Calcular fórmula de Kelly
def calcular_kelly(probabilidad, cuota):
    """
    Calcula la fracción de Kelly recomendada.

    Args:
        probabilidad (float): Probabilidad estimada (ej. 0.70)
        cuota (float): Cuota decimal ofrecida (ej. 1.90)

    Returns:
        float: porcentaje recomendado de apuesta (0 a 1)
    """
    try:
        kelly = (probabilidad * (cuota - 1) - (1 - probabilidad)) / (cuota - 1)
        return max(0, round(kelly, 3))
    except ZeroDivisionError:
        return 0.0
# ✅ 4. Calcular Z-score (riesgo estadístico)
def calcular_z_score(valor, media, desviacion):
    """
    Calcula el Z-score de un valor comparado con su media y desviación estándar.

    Args:
        valor (float): Valor a evaluar
        media (float): Media de referencia
        desviacion (float): Desviación estándar

    Returns:
        float: Z-score redondeado a 2 decimales
    """
    if desviacion == 0:
        return 0.0
    return round((valor - media) / desviacion, 2)
import json
import os
import pandas as pd
from datetime import datetime

# ✅ 5. Filtro y clasificación matemática de picks
def filtrar_picks_validos(picks_json):
    """
    Filtra y clasifica picks con lógica matemática.
    Guarda los aptos en data/picks_validados.json y log en logs/math_log.csv.
    """
    aptos = []
    log_data = []

    for pick in picks_json:
        prob = pick["probabilidad"]
        cuota = pick["cuota"]
        valor = pick["valor"]
        media = pick["media"]
        std = pick["std_dev"]

        ev = calcular_valor_esperado(prob, cuota)
        z = calcular_z_score(valor, media, std)
        kelly = calcular_kelly(prob, cuota)

        estado = "APTO" if ev >= 0.5 and prob >= 0.60 and abs(z) <= 2 else "RECHAZADO"

        pick.update({
            "ev": ev,
            "z_score": z,
            "kelly": kelly,
            "estado": estado
        })

        log_data.append({
            "evento": pick.get("evento", "N/A"),
            "probabilidad": prob,
            "cuota": cuota,
            "ev": ev,
            "z_score": z,
            "kelly": kelly,
            "estado": estado
        })

        if estado == "APTO":
            aptos.append(pick)

    # Guardar picks validados
    os.makedirs("data", exist_ok=True)
    with open("data/picks_validados.json", "w", encoding="utf-8") as f:
        json.dump(aptos, f, ensure_ascii=False, indent=2)

    # Guardar log
    os.makedirs("logs", exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_log = pd.DataFrame(log_data)
    df_log.insert(0, "fecha", now)
    df_log.to_csv("logs/math_log.csv", index=False)

    return aptos
