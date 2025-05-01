import json
import os

def cargar_cuotas_json(ruta="scraping_cuotas/data/cuotas_mlbbulk.json"):
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo de cuotas no encontrado en: {ruta}")
    
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data or len(data) < 3:
        raise ValueError("El archivo de cuotas está vacío o tiene menos de 3 partidos válidos.")

    return data
