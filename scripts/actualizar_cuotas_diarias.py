import sys
import os
sys.path.append(os.path.abspath(".."))

import json
import csv
from datetime import datetime
from pathlib import Path
from ia_engine import procesar_evento

# ✅ Función principal
def actualizar_cuotas_con_datos_realistas():
    try:
        # 📥 Leer cuotas reales
        with open("data/cuotas_mlbbulk.json", "r", encoding="utf-8") as f:
            cuotas = json.load(f)

        # 📥 Leer boletín diario
        with open("data/boletin_diario.json", "r", encoding="utf-8") as f:
            boletin = json.load(f)

        cuotas_diarias = []

        for partido in cuotas:
            local = partido["equipo_local"]
            visitante = partido["equipo_visitante"]

            # 📊 Valores dummy por ahora (luego conectaremos con sabermetría real)
            prob_input = {
                "obp_diff": 0.015,
                "slg_diff": 0.020,
                "woba_diff": 0.018,
                "era_diff": -0.30,
                "fip_diff": -0.25,
                "equipo_local": local
            }

            pred_ia = procesar_evento(prob_input)

            # ✅ Validación para evitar errores si hubo fallo en IA
            if "prediccion" not in pred_ia:
                print(f"⚠️ Pick descartado por error IA: {pred_ia.get('error', 'sin detalle')}")
                continue

            nuevo_pick = {
                "evento": partido["evento"],
                "fecha": partido["fecha"],
                "equipo_local": local,
                "equipo_visitante": visitante,
                "cuota": partido["cuota_local"],
                "probabilidad": pred_ia["prediccion"]["probabilidad_ganador_local"],
                "valor_esperado": round(
                    (pred_ia["prediccion"]["probabilidad_ganador_local"] * partido["cuota_local"]) -
                    (1 - pred_ia["prediccion"]["probabilidad_ganador_local"]), 2),
                "confianza": "Alta" if pred_ia["prediccion"]["probabilidad_ganador_local"] > 0.7 else "Media",
                "pitcher_ok": boletin.get(local, {}).get("riesgo", "") != "alto",
                "clima": partido.get("clima", "Desconocido"),
                "explicacion": pred_ia.get("explicacion", "")
            }

            cuotas_diarias.append(nuevo_pick)

        # 💾 Guardar archivo final del día
        with open("data/cuotas_diarias.json", "w", encoding="utf-8") as f:
            json.dump(cuotas_diarias, f, ensure_ascii=False, indent=2)

        # 📝 Log
        Path("logs").mkdir(exist_ok=True)
        with open("logs/integracion_log.csv", "a", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([now, len(cuotas_diarias), "OK"])

        print(f"✅ {len(cuotas_diarias)} picks integrados y guardados en data/cuotas_diarias.json")

    except Exception as e:
        print(f"❌ Error durante integración: {str(e)}")

# 🚀 Ejecutar
if __name__ == "__main__":
    actualizar_cuotas_con_datos_realistas()
