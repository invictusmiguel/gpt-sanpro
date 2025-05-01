import requests
import os

# Asegúrate que la API Key esté cargada desde el .env
API_KEY = os.getenv("OWM_API_KEY")  # OpenWeatherMap API key

def obtener_clima(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        return {
            "temperatura": data["main"]["temp"],
            "humedad": data["main"]["humidity"],
            "condicion": data["weather"][0]["description"],
            "viento": data["wind"]["speed"]
        }
    except Exception as e:
        return {"error": str(e)}
