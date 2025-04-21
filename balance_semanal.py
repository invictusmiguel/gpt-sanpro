# balance_semanal.py

import json
from datetime import datetime
import os

ARCHIVO_BANCA = "banca.json"
ARCHIVO_HISTORIAL = "datos/historial.json"

def generar_balance_semanal():
    if not os.path.exists(ARCHIVO_BANCA):
        print("❌ Archivo banca.json no encontrado.")
        return

    with open(ARCHIVO_BANCA, "r", encoding="utf-8") as f:
        banca_data = json.load(f)

    saldo = banca_data.get("saldo", 0.0)
    historial = banca_data.get("historial", [])
    recargas = [h for h in historial if h.get("evento") == "recarga"]
    apuestas = [h for h in historial if "apostado" in h]

    total_apostado = sum(a["apostado"] for a in apuestas)
    total_ganancia = sum(a["ganancia"] for a in apuestas)
    ganadas = sum(1 for a in apuestas if a["resultado"] == "ganada")
    perdidas = len(apuestas) - ganadas

    balance_total = total_ganancia - (len(recargas) * 100)
    
    print("📊 BALANCE SEMANAL")
    print(f"📆 Fecha: {datetime.now().date()}")
    print(f"🎯 Apuestas ganadas: {ganadas}")
    print(f"💥 Apuestas perdidas: {perdidas}")
    print(f"💵 Total apostado: {round(total_apostado, 2)} PEN")
    print(f"📈 Ganancia neta: {round(total_ganancia, 2)} PEN")
    print(f"🔁 Recargas efectuadas: {len(recargas)}")
    print(f"🧮 Balance neto: {round(balance_total, 2)} PEN")
    print(f"💰 Saldo final: {round(saldo, 2)} PEN")

if __name__ == "__main__":
    generar_balance_semanal()
