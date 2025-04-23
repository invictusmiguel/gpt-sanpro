from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from datetime import datetime

# 📌 Importaciones necesarias
from utils.mlb.pitchers import get_pitchers_por_partido
from utils.scrapers.auto_savant import enriquecer_con_savant  # Si ya lo tienes
# from utils.clima import obtener_clima  # Si quieres incluir clima

# 📌 Credenciales
USUARIO = "miproyectogol@gmail.com"
CLAVE = "001aef241ED09$"

def extraer_cuotas_mlb():
    # Configura navegador visible
    options = Options()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.bet365.com")
    time.sleep(5)

    # Iniciar sesión
    try:
        login_btn = driver.find_element(By.CSS_SELECTOR, 'div#header-login-link')
        login_btn.click()
        print("🟢 Botón 'Iniciar sesión' clicado.")
    except:
        print("⚠️ No se encontró botón de login. Puede estar visible ya.")

    time.sleep(5)

    try:
        acceder_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Acceder"]')
        acceder_btn.click()
        print("🟢 Botón 'Acceder' presionado.")
        time.sleep(3)
    except Exception as e:
        print(f"⚠️ No se encontró botón de 'Acceder': {e}")

    try:
        campo_email = driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        campo_email.send_keys(USUARIO)
        print("📨 Email ingresado.")

        campo_clave = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        campo_clave.send_keys(CLAVE)
        print("🔐 Contraseña ingresada.")

        btn_login = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        btn_login.click()
        print("✅ Login enviado.")
        time.sleep(5)
    except Exception as e:
        print(f"❌ Error durante el login: {e}")

    time.sleep(5)
    print("✅ Login realizado correctamente, ahora puedes scrapear.")

    # 🔄 Simulación de scraping (debes reemplazar luego con los datos reales del DOM)
    partidos = [
        {"partido": "NY Yankees vs CLE Guardians", "mercado": "Alta", "cuota": 1.85, "confianza": 92},
        {"partido": "SD Padres vs DET Tigers", "mercado": "Baja", "cuota": 1.95, "confianza": 88}
    ]

    # 📌 Añadir pitchers reales
    for p in partidos:
        resultado = get_pitchers_por_partido(p["partido"])
        if "error" not in resultado:
            p["pitcher_local"] = resultado["pitcher_local"]
            p["pitcher_visitante"] = resultado["pitcher_visitante"]
        else:
            p["pitcher_local"] = "N/D"
            p["pitcher_visitante"] = "N/D"
        print(f"✅ Pitchers añadidos para {p['partido']}")

    # 🧠 Añadir enlaces de Savant si está disponible
    try:
        partidos = enriquecer_con_savant(partidos)
        print("🔗 Links de Savant integrados.")
    except Exception as e:
        print(f"⚠️ No se pudo integrar Savant: {e}")

    driver.quit()

    salida = {
        "fecha": datetime.utcnow().isoformat(),
        "partidos": partidos
    }

    with open("data/cuotas_diarias.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    print("✅ Archivo guardado en data/cuotas_diarias.json")
    return salida

if __name__ == "__main__":
    extraer_cuotas_mlb()
