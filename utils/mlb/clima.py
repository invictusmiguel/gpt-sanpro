# utils/clima.py

import requests

# 🌍 API gratuita de OpenWeatherMap (requiere que pongas tu API key aquí)
API_KEY = "TU_API_KEY"  # Sustituye esto por tu clave de openweathermap.org

def obtener_clima(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=es"
        res = requests.get(url)

        if res.status_code != 200:
            return {"error": "No se pudo obtener datos del clima"}

        data = res.json()

        return {
            "temperatura": data["main"]["temp"],
            "humedad": data["main"]["humidity"],
            "viento": data["wind"]["speed"],
            "condicion": data["weather"][0]["description"]
        }
    except Exception as e:
        return {"error": f"Error al consultar clima: {str(e)}"}
