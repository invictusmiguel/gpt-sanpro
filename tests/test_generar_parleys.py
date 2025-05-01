import json
import os
import pytest

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
        for cuota in parley["cuotas"]:
            assert cuota > 1.0
        assert parley["valor_esperado"] >= 0.8

def test_parleys_nivel_3_ev_y_zscore():
    with open(ARCHIVO_SALIDA, "r", encoding="utf-8") as f:
        data = json.load(f)

    for parley in data["nivel_3"]:
        assert parley["valor_esperado"] >= 1.0
        assert -1 <= parley["probabilidad_total"] <= 1

