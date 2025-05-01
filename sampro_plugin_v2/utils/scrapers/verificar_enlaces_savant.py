import json
import requests
from bs4 import BeautifulSoup

def verificar_savant_link(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code != 200:
            return False
        soup = BeautifulSoup(res.text, "lxml")
        return soup.find("table") is not None
    except:
        return False

with open("data/cuotas_diarias.json", "r", encoding="utf-8") as f:
    data = json.load(f)

partidos = data.get("partidos", [])
for partido in partidos:
    for clave in ["savant_local", "savant_visitante"]:
        link = partido.get(clave)
        if link:
            valido = verificar_savant_link(link)
            print(f"🔗 {clave} ({link}) → {'✅ Válido' if valido else '❌ No válido'}")
