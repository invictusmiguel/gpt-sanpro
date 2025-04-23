from utils.scrapers.savant_scraper import get_pitcher_savant_stats

url = "https://baseballsavant.mlb.com/savant-player/garrett-cole-543037"
stats = get_pitcher_savant_stats(url)
print(stats)
