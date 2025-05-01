from playwright.sync_api import sync_playwright
import json

def get_odds_oddspedia() -> list[dict]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://oddspedia.com/es/beisbol/eeuu/mlb/cuotas")

        page.wait_for_selector("div.match-list-item.match-list-item--with-odds", timeout=15000)
        page.evaluate("() => window.scrollBy(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)

        matches = page.locator("div.match-list-item.match-list-item--with-odds").all()
        print(f"🎯 Partidos encontrados: {len(matches)}")

        data: list[dict] = []

        for match in matches:
            teams = match.locator("div.match-team__name").all_inner_texts()
            odds = match.locator("span.odd__value").all_inner_texts()
            if len(teams) == 2 and len(odds) >= 2:
                data.append({
                    "home": teams[0],
                    "away": teams[1],
                    "odds_home": odds[0],
                    "odds_away": odds[1]
                })

        browser.close()
        return data
