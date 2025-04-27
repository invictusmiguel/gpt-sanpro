import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

print("✅ Script de scraping MLB iniciado")

def get_driver():
    """Configura y retorna el driver de Chrome con opciones anti-detección"""
    chrome_options = Options()
    
    # Opciones para evitar detección
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    
    # Ruta al chromedriver (asegúrate de tenerlo en la misma carpeta)
    service = Service('chromedriver.exe')
    
    return webdriver.Chrome(service=service, options=chrome_options)

def login_bet365(driver, username, password):
    """Maneja el proceso de login en Bet365"""
    print("🔑 Intentando login...")
    try:
        driver.get("https://www.bet365.pe/#/HO/")
        
        # Esperar y hacer click en botón de login
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".hm-MainHeaderRHSLoggedOutWide_Login"))
        ).click()
        
        # Rellenar credenciales
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        ).send_keys(username)
        
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password)
        
        # Enviar formulario
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Esperar login completo
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".hm-MainHeaderRHSLoggedInWide_Account"))
        )
        print("✅ Login exitoso")
        
        # Delay aleatorio para parecer humano
        time.sleep(random.uniform(2, 4))
        
    except Exception as e:
        print(f"❌ Fallo en login: {str(e)}")
        driver.save_screenshot("login_error.png")
        raise

def navigate_to_mlb(driver):
    """Navega a la sección de MLB"""
    print("⚾ Navegando a MLB...")
    try:
        # Click en menú de deportes
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".sm-SportsButton_Label"))
        ).click()
        
        # Seleccionar béisbol
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Béisbol') or contains(., 'MLB')]"))
        ).click()
        
        # Esperar carga
        time.sleep(random.uniform(3, 5))
        print("✅ Sección MLB cargada")
        
    except Exception as e:
        print(f"❌ Error navegando a MLB: {str(e)}")
        driver.save_screenshot("mlb_nav_error.png")
        raise

def scrape_mlb_games(driver):
    """Extrae datos de partidos y cuotas"""
    print("📊 Extrayendo datos de partidos...")
    try:
        # Esperar a que carguen los partidos
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".gl-MarketGroupContainer"))
        )
        
        games = driver.find_elements(By.CSS_SELECTOR, ".gl-MarketGroupContainer")
        data = []
        
        for game in games:
            try:
                # Extraer nombres de equipos
                teams = game.find_element(By.CSS_SELECTOR, ".gl-Participant_Name").text
                
                # Extraer cuotas
                odds = game.find_elements(By.CSS_SELECTOR, ".gl-Participant_General")
                home_odd = odds[0].text if len(odds) > 0 else "N/A"
                away_odd = odds[1].text if len(odds) > 1 else "N/A"
                
                data.append({
                    'Partido': teams,
                    'Cuota Local': home_odd,
                    'Cuota Visitante': away_odd,
                    'Hora': time.strftime("%H:%M"),
                    'Fecha': time.strftime("%Y-%m-%d")
                })
                
                # Delay aleatorio entre partidos
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"⚠️ Error procesando partido: {str(e)}")
                continue
        
        return data
        
    except Exception as e:
        print(f"❌ Error en scraping: {str(e)}")
        driver.save_screenshot("scrape_error.png")
        raise

def save_to_csv(data, filename="mlb_odds.csv"):
    """Guarda los datos en CSV"""
    df = pd.DataFrame(data)
    
    # Si el archivo existe, agregar nuevos datos
    if os.path.exists(filename):
        existing_df = pd.read_csv(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"💾 Datos guardados en {filename}")

def main():
    driver = None
    try:
        # Configurar driver
        driver = get_driver()
        
        # Credenciales (MODIFICAR CON TUS DATOS)
        USERNAME = "miproyectogol@gmial.com"
        PASSWORD = "001AEF241ed09$"
        
        # Flujo principal
        login_bet365(driver, USERNAME, PASSWORD)
        navigate_to_mlb(driver)
        games_data = scrape_mlb_games(driver)
        
        if games_data:
            save_to_csv(games_data)
            print("\n📋 Resumen de datos:")
            print(pd.DataFrame(games_data))
        else:
            print("⚠️ No se encontraron partidos disponibles")
        
        input("\nPresiona ENTER para cerrar...")
        
    except Exception as e:
        print(f"\n❌ Error fatal: {str(e)}")
        
    finally:
        if driver:
            driver.quit()
            print("🧹 Navegador cerrado")

if __name__ == "__main__":
    main()