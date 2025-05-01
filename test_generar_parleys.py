# test_generar_parleys.py

import json
import os

ARCHIVO_SALIDA = "data/parleys_por_nivel.json"

def test_archivo_generado_existe():
    assert os.path.exists(ARCHIVO_SALIDA), "No se generó el archivo de salida"

def test_estructura_general():
    with open(ARCHIVO_SALIDA, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "nivel_1" in data
    assert "nivel_2" in data
    assert "nivel_3" in data

def test_parleys_nivel_2_ev_presente():
    with open(ARCHIVO_SALIDA, "r", encoding="utf-8") as f:
        data = json.load(f)

    for parley in data["nivel_2"]:
        assert parley["valor_esperado"] >= 0.8

def test_parleys_nivel_3_ev_y_zscore():
    with open(ARCHIVO_SALIDA, "r", encoding="utf-8") as f:
        data = json.load(f)

    for parley in data["nivel_3"]:
        assert parley["valor_esperado"] >= 1.0
        assert -1 <= parley["probabilidad_total"] <= 1
def test_eventos_unicos_en_parley():
    with open(ARCHIVO_SALIDA, "r", encoding="utf-8") as f:
        data = json.load(f)

    for nivel in ["nivel_1", "nivel_2", "nivel_3"]:
        for parley in data[nivel]:
            eventos = parley["combinacion"]
            assert len(eventos) == len(set(eventos)), f"Eventos duplicados en {nivel}: {eventos}"
import json
import os

ARCHIVO_PICKS = "data/picks_validados.json"

def test_archivo_picks_existe():
    assert os.path.exists(ARCHIVO_PICKS), "No existe data/picks_validados.json"

def test_picks_tienen_campos_requeridos():
    with open(ARCHIVO_PICKS, "r", encoding="utf-8") as f:
        picks = json.load(f)

    campos_requeridos = ["evento", "probabilidad", "cuota"]
    for p in picks:
        for campo in campos_requeridos:
            assert campo in p, f"Falta el campo '{campo}' en el pick: {p}"
