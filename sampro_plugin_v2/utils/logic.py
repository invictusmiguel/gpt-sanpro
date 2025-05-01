import random

def generar_parley(partidos):
    if not partidos or len(partidos) < 3:
        return "No hay suficientes partidos hoy para un parley."

    seleccionados = partidos[:3]  # Los primeros 3 partidos

    combinadas = []
    cuota_total = 1.0

    for p in seleccionados:
        local = p['teams']['home']['name']
        visitante = p['teams']['away']['name']
        equipo = random.choice([local, visitante])
        cuota = round(random.uniform(1.5, 2.5), 2)  # Simula cuota realista

        combinadas.append(f"{equipo} gana (cuota: {cuota})")
        cuota_total *= cuota

    return (
        "🎯 Parley sugerido:\n" +
        "\n".join(combinadas) +
        f"\n\n💰 Cuota total estimada: {round(cuota_total, 2)}"
    )

def calcular_valor(prob_real=0.6, cuota=2.1):
    valor = (prob_real * cuota) - 1
    return f"📊 Valor Esperado: {round(valor, 2)} (con cuota {cuota} y probabilidad {prob_real*100}%)"
