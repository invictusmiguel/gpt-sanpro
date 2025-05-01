import json
import os
from datetime import date

def cargar_json(path: str):
    if not os.path.exists(path):
        print(f"[ERROR] Archivo no encontrado: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def parley_es_acertado(parley: dict, resultados: dict) -> bool:
    eventos = parley["combinacion"]
    for evento in eventos:
        if resultados.get(evento) != evento.split(" vs ")[0] and resultados.get(evento) != evento.split(" vs ")[1]:
            return False
    return True

def evaluar_nivel(parleys: list, resultados_dict: dict) -> dict:
    aciertos = 0
    total = len(parleys)
    evs = []
    ganancia_total = 0
    inversion_total = total  # se supone 1 unidad por parley

    for parley in parleys:
        evs.append(parley.get("valor_esperado", 0))
        if parley_es_acertado(parley, resultados_dict):
            aciertos += 1
            ganancia_total += parley["cuota_total"]
    
    fallos = total - aciertos
    porcentaje_exito = round(aciertos / total, 3) if total else 0
    roi = round((ganancia_total - inversion_total) / inversion_total, 3) if inversion_total else 0
    ev_real = round(sum(evs) / len(evs), 3) if evs else 0

    return {
        "aciertos": aciertos,
        "fallos": fallos,
        "porcentaje_exito": porcentaje_exito,
        "roi": roi,
        "ev_real_promedio": ev_real
    }

def mostrar_dashboard(fecha: str, evaluacion: dict):
    print(f"\n[INFO] Evaluación – {fecha}")
    for nivel, datos in evaluacion.items():
        if datos["roi"] > 0.5:
            color = "[ALTO]"
        elif datos["roi"] > 0:
            color = "[MEDIO]"
        else:
            color = "[BAJO]"
        print(f"{color} {nivel.capitalize()} – ROI: {datos['roi']*100:.0f}%, Éxito: {int(datos['porcentaje_exito']*100)}%")
    mejor = max(evaluacion.items(), key=lambda x: x[1]["roi"])[0]
    print(f"\n>> {mejor.capitalize()} es el más rentable en este ciclo\n")

def main():
    parleys = cargar_json("data/parleys_por_nivel.json")
    resultados = cargar_json("data/resultados_reales.json")
    if not parleys or not resultados:
        return

    resultados_dict = {r["evento"]: r["ganador_real"] for r in resultados}
    fecha = parleys.get("fecha", str(date.today()))
    evaluacion = {}

    for nivel in ["nivel_1", "nivel_2", "nivel_3"]:
        evaluacion[nivel] = evaluar_nivel(parleys[nivel], resultados_dict)

    # Guardar resultados
    with open("data/evaluacion_resultados.json", "w", encoding="utf-8") as f:
        json.dump({"fecha": fecha, **evaluacion}, f, indent=2, ensure_ascii=False)

    # Actualizar CSV log
    with open("logs/evaluacion_predictiva.csv", "a", encoding="utf-8") as f:
        linea = f"{fecha}," + ",".join(
            f"{evaluacion[n]['aciertos']};{evaluacion[n]['fallos']};{evaluacion[n]['roi']};{evaluacion[n]['porcentaje_exito']}"
            for n in ["nivel_1", "nivel_2", "nivel_3"]
        )
        f.write(linea + "\n")

    mostrar_dashboard(fecha, evaluacion)

if __name__ == "__main__":
    main()
