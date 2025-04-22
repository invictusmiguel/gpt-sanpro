import random

def predecir_super_altas_bajas(partidos, linea_total=8.5):
    """
    partidos = lista de dicts con claves: {"carreras_local": int, "carreras_visita": int}
    """
    if len(partidos) < 2:
        return {"error": "Se requieren al menos 2 enfrentamientos previos."}

    total_carreras = [p["carreras_local"] + p["carreras_visita"] for p in partidos]
    promedio = sum(total_carreras) / len(total_carreras)

    return {
        "over_under": "Over" if promedio > linea_total else "Under",
        "promedio_total_carreras": round(promedio, 2),
        "linea": linea_total,
        "confianza": "Alta" if abs(promedio - linea_total) > 1 else "Media"
    }
