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
