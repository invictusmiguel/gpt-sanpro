print("🔥 Script funcionando!")

# Importar selenium (asegúrate de tenerlo instalado con: pip install selenium)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
print("✅ Selenium importado correctamente")

# Configurar opciones de Chrome
options = Options()
options.add_argument("--headless")  # Ejecución sin interfaz gráfica
options.add_argument("--disable-gpu")  # Mejor rendimiento en headless
options.add_argument("--no-sandbox")  # Necesario en algunos sistemas

# Inicializar el driver (asegúrate de tener chromedriver.exe en la misma carpeta)
driver = webdriver.Chrome(options=options)
print("🚀 Navegador Chrome iniciado en modo headless")

try:
    print("🌐 Cargando página...")
    driver.get("https://www.google.com")
    print(f"📄 Título de la página: {driver.title}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    
finally:
    driver.quit()
    print("🧹 Navegador cerrado correctamente")