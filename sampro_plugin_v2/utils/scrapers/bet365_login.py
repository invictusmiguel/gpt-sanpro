# utils/scrapers/bet365_login.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time

def iniciar_sesion_bet365():
    print("🌐 Iniciando Chrome con configuración anti-bloqueo...")

    # Ruta al perfil real de Chrome (ajústala si usas otro)
    user_profile = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")

    options = Options()
    options.add_argument(f"user-data-dir={user_profile}")
    options.add_argument("profile-directory=Default")
    options.add_argument("--start-maximized")

    # 🛡️ Ocultamos señales de bot
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Ruta del ChromeDriver (ajusta si lo mueves)
    service = Service("C:/Users/mario/Documents/apuestas/chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    # Inyectamos JS para ocultar automatización
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            });
        """
    })

    # Vamos directo a Bet365
    print("🔗 Navegando a https://www.bet365.com...")
    driver.get("https://www.bet365.com/#/HO/")

    # Esperamos que aparezca algún componente clave
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "hm-MainHeaderRHSLoggedOutWide_LoginContainer"))
        )
        print("✅ Bet365 cargó correctamente.")
    except:
        print("⚠️ Advertencia: Bet365 no cargó correctamente o la clase no se encontró.")

    # ⏳ Damos tiempo extra por si hay overlays
    time.sleep(5)

    return driver

    # Paso extra: si aparece el modal de "Continuar", lo clicamos
    try:
        print("🧭 Verificando si aparece el modal de 'Último acceso'...")
        continuar_btn = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "llm-LastLoginModule_Button"))
        )
        continuar_btn.click()
        print("✅ Botón 'Continuar' clicado correctamente.")
        time.sleep(3)
    except:
        print("ℹ️ No apareció el modal de 'Continuar', seguimos sin problema.")
