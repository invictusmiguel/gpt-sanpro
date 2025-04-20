import random

def simular_apuestas(n=10000, prob_real=0.6, cuota=2.0):
    ganadas = 0
    ganancias = 0
    perdidas = 0

    for _ in range(n):
        apuesta = random.random() < prob_real
        if apuesta:
            ganadas += 1
            ganancias += (cuota - 1)
        else:
            perdidas += 1
            ganancias -= 1

    roi = ganancias / n
    kelly = calcular_kelly(prob_real, cuota)

    return (
        f"🧠 Simulación de {n} apuestas\n"
        f"✔️ Ganadas: {ganadas}\n"
        f"❌ Perdidas: {perdidas}\n"
        f"📈 ROI estimado: {round(roi*100, 2)}%\n"
        f"📊 Kelly Criterion sugerido: {round(kelly*100, 2)}% del bankroll"
    )

def calcular_kelly(prob, cuota):
    b = cuota - 1
    q = 1 - prob
    kelly = (b * prob - q) / b
    return max(kelly, 0)
