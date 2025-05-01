# parsing_utils.py
# 🧰 Funciones auxiliares para scraping: limpieza de HTML y logging

import re
import csv
from datetime import datetime

def clean_text(text):
    """ 🧹 Elimina espacios, saltos de línea y etiquetas HTML """
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)  # Reemplaza múltiples espacios/saltos por uno solo
    text = re.sub(r'<.*?>', '', text)  # Quita etiquetas HTML (si quedaran)
    return text.strip()


def log_execution(log_path, success=True, error=""):
    """ 📝 Guarda un log en formato CSV con cada ejecución """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "OK" if success else "ERROR"
    
    row = [now, status, error]
    
    try:
        with open(log_path, mode="a", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(row)
    except Exception as e:
        print(f"❌ No se pudo escribir en el log: {e}")
