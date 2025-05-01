from flask import Blueprint, request, jsonify
from utils.cuotas import cargar_cuotas_json
import datetime
import os

bp = Blueprint("parley_seguro_vida", __name__)

@bp.route("/parley_seguro_vida", methods=["GET"])
def generar_parleys():
    modo = request.args.get("modo", "").lower()
    umbral_min = 0
    umbral_max = float("inf")

    if modo == "conservador":
        umbral_min, umbral_max = 3.0, 6.0
    elif modo == "riesgo":
        umbral_min = 6.0

    try:
        cuotas = cargar_cuotas_json()
        parlays = []

        for i in range(len(cuotas)):
            for j in range(i+1, len(cuotas)):
                for k in range(j+1, len(cuotas)):
                    p1, p2, p3 = cuotas[i], cuotas[j], cuotas[k]
                    try:
                        cuota_total = float(p1["odds_home"]) * float(p2["odds_home"]) * float(p3["odds_home"])
                        if umbral_min <= cuota_total <= umbral_max:
                            parlays.append({
                                "partidos": [
                                    f"{p1['home']} vs {p1['away']}",
                                    f"{p2['home']} vs {p2['away']}",
                                    f"{p3['home']} vs {p3['away']}"
                                ],
                                "cuota_total": round(cuota_total, 2)
                            })
                    except:
                        continue

        return jsonify(parlays)

    except Exception as e:
        log_error(str(e))
        return jsonify({"error": str(e)}), 400


def log_error(mensaje: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
    log_path = "logs/cuotas_consumo_log.csv"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{now},ERROR,\"{mensaje}\"\n")
