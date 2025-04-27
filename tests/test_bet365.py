from utils.scrapers.bet365_login import iniciar_sesion_bet365
from utils.scrapers.bet365_login import iniciar_sesion_bet365
from utils.scrapers.bet365_scraper_mlb import scrapear_cuotas_alternativas

driver = iniciar_sesion_bet365()
cuotas = scrapear_cuotas_alternativas(driver)

for cuota in cuotas:
    print(cuota)

driver.quit()
