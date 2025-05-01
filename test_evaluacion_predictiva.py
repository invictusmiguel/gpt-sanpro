import json
import os
from datetime import date

JSON_PATH = "data/evaluacion_resultados.json"
CSV_PATH = "logs/evaluacion_predictiva.csv"

def test_json_generado_existe():
    assert os.path.exists(JSON_PATH), "No se generó evaluacion_resultados.json"

def test_estructura_json_valida():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "fecha" in data
    for nivel in ["nivel_1", "nivel_2", "nivel_3"]:
        assert nivel in data
        stats = data[nivel]
        assert all(k in stats for k in ["aciertos", "fallos", "porcentaje_exito", "roi", "ev_real_promedio"])

def test_csv_actualizado():
    hoy = str(date.today())
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    assert any(hoy in l for l in lineas), "No se registró la fecha de hoy en el CSV"
