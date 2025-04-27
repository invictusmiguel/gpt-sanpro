import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import json

class Bet365Bot:
    def __init__(self):
        self.driver = None
        self.config = self.load_config()
        self.setup_driver()
        
    def load_config(self):
        """Carga configuración desde archivo config.json"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Archivo config.json no encontrado. Usando valores por defecto.")
            return {
                "username": "miproyectogol@gmail.com",
                "password": "001AEF241ed09$",
                "headless": False,
                "timeout": 20,
                "screenshots": True
            }
    
    def setup_driver(self):
        """Configura el driver de Chrome con opciones personalizadas"""
        print("🛠️ Configurando navegador...")
        chrome_options = Options()
        
        # Configuración anti-detección
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument(f"user-agent={self.get_random_user_agent()}")
        
        if self.config.get("headless", False):
            chrome_options.add_argument("--headless=new")
        
        # Configuración del servicio
        service = Service('chromedriver.exe')
        
        try:
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ Navegador configurado correctamente")
        except Exception as e:
            print(f"❌ Error al iniciar el navegador: {str(e)}")
            raise

    def get_random_user_agent(self):
        """Genera un user-agent aleatorio"""
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        return random.choice(agents)

    def random_delay(self, min_sec=1, max_sec=3):
        """Delay aleatorio para simular comportamiento humano"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def login(self):
        """Maneja el proceso de login en Bet365"""
        print("🔑 Iniciando sesión...")
        try:
            self.driver.get("https://www.bet365.pe/#/HO/")
            self.random_delay(2, 4)

            # Localizar y hacer click en botón de login
            login_btn = WebDriverWait(self.driver, self.config["timeout"]).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".hm-MainHeaderRHSLoggedOutWide_Login"))
            )
            login_btn.click()
            self.random_delay()

            # Ingresar credenciales
            username_field = WebDriverWait(self.driver, self.config["timeout"]).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
            )
            username_field.send_keys(self.config["username"])
            self.random_delay(0.5, 1.5)

            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_field.send_keys(self.config["password"])
            self.random_delay(0.5, 1.5)

            # Enviar formulario
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()

            # Verificar login exitoso
            WebDriverWait(self.driver, self.config["timeout"]).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".hm-MainHeaderRHSLoggedInWide_Account"))
            )
            print("✅ Login exitoso")
            self.random_delay(3, 5)
            
        except Exception as e:
            if self.config["screenshots"]:
                self.driver.save_screenshot("login_error.png")
            print(f"❌ Error en login: {str(e)}")
            raise

    def navigate_to_sport(self, sport_name="Béisbol"):
        """Navega a la sección del deporte especificado"""
        print(f"⚾ Navegando a {sport_name}...")
        try:
            # Abrir menú de deportes
            sports_menu = WebDriverWait(self.driver, self.config["timeout"]).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".sm-SportsButton_Label"))
            )
            sports_menu.click()
            self.random_delay()

            # Seleccionar deporte
            sport_option = WebDriverWait(self.driver, self.config["timeout"]).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[contains(., '{sport_name}')]"))
            )
            sport_option.click()
            
            # Esperar carga
            WebDriverWait(self.driver, self.config["timeout"]).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".gl-MarketGroupContainer"))
            )
            print(f"✅ Sección {sport_name} cargada")
            self.random_delay(2, 4)
            
        except Exception as e:
            if self.config["screenshots"]:
                self.driver.save_screenshot(f"{sport_name.lower()}_nav_error.png")
            print(f"❌ Error navegando a {sport_name}: {str(e)}")
            raise

    def scrape_odds(self):
        """Extrae las cuotas de los partidos disponibles"""
        print("📊 Extrayendo cuotas...")
        try:
            games = WebDriverWait(self.driver, self.config["timeout"]).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".gl-MarketGroupContainer"))
            )
            
            data = []
            for game in games:
                try:
                    # Extraer información del partido
                    teams = game.find_element(By.CSS_SELECTOR, ".gl-Participant_Name").text
                    odds = game.find_elements(By.CSS_SELECTOR, ".gl-Participant_General")
                    
                    if len(odds) >= 2:
                        data.append({
                            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Partido": teams,
                            "Local": odds[0].text,
                            "Visitante": odds[1].text,
                            "Empate": odds[2].text if len(odds) > 2 else "N/A"
                        })
                    
                    self.random_delay(0.3, 1.2)
                    
                except Exception as e:
                    print(f"⚠️ Error procesando partido: {str(e)}")
                    continue
            
            return data
            
        except Exception as e:
            if self.config["screenshots"]:
                self.driver.save_screenshot("scrape_error.png")
            print(f"❌ Error en scraping: {str(e)}")
            raise

    def save_data(self, data, filename="bet365_odds.csv"):
        """Guarda los datos en un archivo CSV"""
        try:
            df = pd.DataFrame(data)
            
            # Si el archivo existe, agregar nuevos datos
            if os.path.exists(filename):
                existing_df = pd.read_csv(filename)
                df = pd.concat([existing_df, df], ignore_index=True)
            
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"💾 Datos guardados en {filename}")
            
        except Exception as e:
            print(f"❌ Error guardando datos: {str(e)}")
            raise

    def run(self):
        """Ejecuta el flujo completo del bot"""
        try:
            self.login()
            self.navigate_to_sport("Béisbol")
            odds_data = self.scrape_odds()
            
            if odds_data:
                self.save_data(odds_data)
                print("\n📋 Resumen de datos obtenidos:")
                print(pd.DataFrame(odds_data))
            else:
                print("⚠️ No se encontraron partidos disponibles")
                
            input("\nPresiona ENTER para cerrar el navegador...")
            
        except Exception as e:
            print(f"\n❌ Error en la ejecución: {str(e)}")
            
        finally:
            if self.driver:
                self.driver.quit()
                print("🧹 Navegador cerrado")

if __name__ == "__main__":
    print("🚀 Iniciando Bot Bet365")
    bot = Bet365Bot()
    bot.run()