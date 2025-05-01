# utils/scrapers/bet365_login.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time

def iniciar_sesion_bet365():
    print("🌐 Abriendo navegador Chrome con perfil de usuario real...")

    # Ruta al perfil de Chrome actual (ajustado para Windows)
    user_profile = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
    
    options = Options()
    options.add_argument(f"user-data-dir={user_profile}")  # Usa perfil real
    options.add_argument("profile-directory=Default")       # Ajusta si usas otro perfil
    options.add_argument("--start-maximized")

    # ⚠️ Desactiva señales de automatización
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # ❌ NO usar headless, Bet365 bloquea eso
    # options.add_argument("--headless=new")

    # Ruta al ChromeDriver
    driver_path = "C:/Users/mario/Documents/apuestas/chromedriver/chromedriver.exe"
    service = Service(driver_path)

    # Abre Chrome con todo configurado
    driver = webdriver.Chrome(service=service, options=options)

    # Carga el sitio y espera que cargue visualmente
    driver.get("https://www.bet365.com/")
    time.sleep(10)

    return driver
