import sys
sys.path.append("C:/Users/mario/Documents/apuestas")

from gpt_sanpro.scrapers.espn_pitcher_scraper import get_pitcher_stats_espn

url = "https://www.espn.com/mlb/player/stats/_/id/33039/garrett-cole"
stats = get_pitcher_stats_espn(url)
print(stats)
