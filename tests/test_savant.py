from utils.scrapers.savant_scraper import get_pitcher_savant_stats

# URL del perfil Baseball Savant (👨‍💻 Cambia si necesitas otro jugador)
url = "https://baseballsavant.mlb.com/savant-player/garrett-cole-543037?stats=statcast-r-pitching-mlb"

print("📊 Resultados desde Baseball Savant:")
stats = get_pitcher_savant_stats(url)

for key, val in stats.items():
    print(f"{key}: {val}")
