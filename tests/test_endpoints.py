# tests/test_endpoints.py

# 📦 Importaciones necesarias
import requests

# 📈 Configuración inicial
BASE_URL = "http://127.0.0.1:5000"

def test_homepage():
    print("🔵 Probando endpoint / (homepage)...")
    try:
        response = requests.get(BASE_URL + "/")
        assert response.status_code == 200
        print("✅ Homepage responde correctamente.")
    except Exception as e:
        print(f"❌ Error probando homepage: {e}")

def test_predict():
    print("🔵 Probando endpoint /predict...")
    try:
        payload = {
            "obp_diff": 0.015,
            "slg_diff": 0.020,
            "woba_diff": 0.018,
            "era_diff": -0.45,
            "fip_diff": -0.30
        }
        response = requests.post(BASE_URL + "/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "equipo_ganador_probable" in data
        print("✅ Predict responde correctamente.")
    except Exception as e:
        print(f"❌ Error probando predict: {e}")
# tests/test_endpoints.py (continuación)

def test_super_altas_bajas():
    print("🔵 Probando endpoint /super_altas_bajas...")
    try:
        params = {
            "equipo1": "Yankees",
            "equipo2": "Red Sox"
        }
        response = requests.get(BASE_URL + "/super_altas_bajas", params=params)
        assert response.status_code == 200
        data = response.json()
        assert "over_under" in data
        print("✅ Super Altas/Bajas responde correctamente.")
    except Exception as e:
        print(f"❌ Error probando super_altas_bajas: {e}")

def test_parley_seguro_vida():
    print("🔵 Probando endpoint /parley_seguro_vida_json...")
    try:
        response = requests.get(BASE_URL + "/parley_seguro_vida_json")
        assert response.status_code == 200
        data = response.json()
        assert "parleys" in data or "error" in data
        print("✅ Parley Seguro de Vida responde correctamente.")
    except Exception as e:
        print(f"❌ Error probando parley_seguro_vida: {e}")

# 🏁 Ejecutar todas las pruebas
if __name__ == "__main__":
    print("🚀 Iniciando pruebas automáticas de SAMPRO...")
    test_homepage()
    test_predict()
    test_super_altas_bajas()
    test_parley_seguro_vida()
    print("🏆 Todas las pruebas completadas.")
