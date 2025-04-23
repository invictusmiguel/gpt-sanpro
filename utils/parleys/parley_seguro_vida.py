import hashlib
from datetime import datetime, timezone
from functools import reduce

from utils.mlb.historial import get_historial_enfrentamientos
from utils.mlb.pitchers import get_pitchers_por_partido
from utils.mlb.ubicaciones import MAPA_ESTADIOS
from utils.clima import obtener_clima
from utils.scrapers.savant_scraper import get_pitcher_savant_stats

def obtener_era_pitcher(pitcher):
    if isinstance(pitcher, dict):
        return pitcher.get("era")
    return None

def clasificar_picks(picks):
    alta, media, baja = [], [], []
    for pick in picks:
        conf = pick.get('confianza', 0)
        if conf >= 85:
            alta.append(pick)
        elif 70 <= conf < 85:
            media.append(pick)
        else:
            baja.append(pick)
    return alta, media, baja

def probabilidad_parley(lista_probabilidades):
    if not lista_probabilidades:
        return 0
    return round(reduce(lambda a, b: a * b, lista_probabilidades), 4)

def valor_esperado(prob, cuota):
    return round((prob * cuota) - 1, 3)

def calcular_cuota_total(picks):
    cuotas = [float(p.get('cuota', 0)) for p in picks if p.get('cuota')]
    if not cuotas:
        return 0
    return round(reduce(lambda a, b: a * b, cuotas), 2)

def generar_codigo(picks):
    base = "-".join(p.get('partido', '') for p in picks) + datetime.now(timezone.utc).isoformat()
    return hashlib.sha256(base.encode()).hexdigest()[:10].upper()

def generar_parleys_seguro_vida(picks, inversion_total=50):
    for pick in picks:
        partido = pick.get("partido", "")
        if "vs" in partido:
            equipos = partido.split(" vs ")
            if len(equipos) == 2:
                equipo1, equipo2 = equipos[0].strip(), equipos[1].strip()

                # 🧠 Historial
                historial = get_historial_enfrentamientos(equipo1, equipo2)
                if isinstance(historial, dict):
                    promedio = historial.get("promedio_carreras", 0)
                    if promedio >= 8.0:
                        pick["confianza"] += 3
                    elif promedio <= 6.5:
                        pick["confianza"] -= 2

                # ⚾ Pitchers (ERA)
                pitchers = get_pitchers_por_partido(partido)
                if isinstance(pitchers, dict):
                    era_local = obtener_era_pitcher(pitchers.get("pitcher_local"))
                    era_visit = obtener_era_pitcher(pitchers.get("pitcher_visitante"))

                    if era_local is not None:
                        pick["confianza"] += 2 if era_local <= 2.80 else -2 if era_local >= 5 else 0
                    if era_visit is not None:
                        pick["confianza"] += 2 if era_visit <= 2.80 else -2 if era_visit >= 5 else 0

                # 🌦️ Clima
                coords = MAPA_ESTADIOS.get(equipo1)
                if coords:
                    clima = obtener_clima(coords["lat"], coords["lon"])
                    if isinstance(clima, dict):
                        if clima.get("condicion", "").lower() in ["lluvia", "tormenta"]:
                            pick["confianza"] -= 3
                        if clima.get("viento", 0) >= 6:
                            pick["confianza"] -= 2
                        if clima.get("temperatura", 20) < 10:
                            pick["confianza"] -= 1

                # 📊 Baseball Savant (si hay URL en pick)
                savant_url = pick.get("savant_url")
                if savant_url:
                    stats = get_pitcher_savant_stats(savant_url)
                    if stats:
                        xera = stats.get("xERA")
                        csw = stats.get("CSW%")
                        whiff = stats.get("Whiff%")
                        if xera and xera < 3:
                            pick["confianza"] += 2
                        elif xera and xera > 4.5:
                            pick["confianza"] -= 2
                        if csw and csw > 30:
                            pick["confianza"] += 1
                        if whiff and whiff > 30:
                            pick["confianza"] += 1

                pick["confianza"] = min(max(pick["confianza"], 50), 100)

    alta, media, baja = clasificar_picks(picks)
    parlays = []

    # 🎯 Parley 1 – Máxima Selección
    parley1 = (alta + media)[:12]
    if len(parley1) < 10:
        return [{"error": "No hay suficientes selecciones para el Parley Máximo (mínimo 10)."}]
    cuota1 = calcular_cuota_total(parley1)
    prob1 = probabilidad_parley([p.get("confianza", 0) / 100 for p in parley1])
    ve1 = valor_esperado(prob1, cuota1)

    # 🎯 Parley 2 – Recomendado
    parley2 = alta[:8]
    cuota2 = calcular_cuota_total(parley2)
    prob2 = probabilidad_parley([p.get("confianza", 0) / 100 for p in parley2])
    ve2 = valor_esperado(prob2, cuota2)

    # 🎯 Parley 3 – Seguro de Vida
    parley3 = sorted(picks, key=lambda x: x.get("confianza", 0), reverse=True)[:4]
    if len(parley3) < 2:
        return [{"error": "No hay suficientes selecciones para el Parley Seguro (mínimo 2)."}]
    cuota3 = calcular_cuota_total(parley3)
    prob3 = probabilidad_parley([p.get("confianza", 0) / 100 for p in parley3])
    ve3 = valor_esperado(prob3, cuota3)

    # 💰 Distribución
    distribucion = [0.4, 0.3, 0.3]
    parlays.append({
        "nombre": "Máxima Selección",
        "picks": parley1,
        "cuota_total": cuota1,
        "probabilidad": prob1,
        "valor_esperado": ve1,
        "inversion": round(inversion_total * distribucion[0], 2),
        "codigo_sampro": generar_codigo(parley1)
    })

    parlays.append({
        "nombre": "Recomendado SAMPRO",
        "picks": parley2,
        "cuota_total": cuota2,
        "probabilidad": prob2,
        "valor_esperado": ve2,
        "inversion": round(inversion_total * distribucion[1], 2),
        "codigo_sampro": generar_codigo(parley2)
    })

    parlays.append({
        "nombre": "Seguro de Vida",
        "picks": parley3,
        "cuota_total": cuota3,
        "probabilidad": prob3,
        "valor_esperado": ve3,
        "inversion": round(inversion_total * distribucion[2], 2),
        "codigo_sampro": generar_codigo(parley3)
    })

    return parlays
