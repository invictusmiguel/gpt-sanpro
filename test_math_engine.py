import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from gpt_sanpro.calculo_matematico import filtrar_picks_validos

# 🧪 Lista de picks simulados para prueba
picks = [
    {
        "evento": "Yankees vs Red Sox",
        "probabilidad": 0.72,
        "cuota": 1.90,
        "valor": 1.85,
        "media": 1.65,
        "std_dev": 0.15
    },
    {
        "evento": "Mets vs Dodgers",
        "probabilidad": 0.55,
        "cuota": 1.70,
        "valor": 2.20,
        "media": 1.65,
        "std_dev": 0.20
    }
]

# 🧠 Ejecutamos el filtro
resultado = filtrar_picks_validos(picks)

# 🔍 Imprimimos lo que se validó como APTO
from pprint import pprint
print("✅ Picks APTOS:")
pprint(resultado)
