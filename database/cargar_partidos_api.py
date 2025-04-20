import requests
import sqlite3

API_KEY = 'cef9115ecad4dcadf30573ca8c3d3abe'  # tu key gratuita API-Football
URL = 'https://v3.football.api-sports.io/fixtures'
HEADERS = {'x-apisports-key': API_KEY}

params = {
    'league': 39,     # Premier League
    'season': 2023
}

conn = sqlite3.connect('database/partidos.db')
cursor = conn.cursor()

response = requests.get(URL, headers=HEADERS, params=params)

if response.status_code == 200:
    data = response.json()
    partidos = data['response']

    for p in partidos:
        fixture = p['fixture']
        teams = p['teams']
        goals = p['goals']
        league = p['league']

        fecha = fixture['date'][:10]
        local = teams['home']['name']
        visita = teams['away']['name']
        goles_local = goals['home'] if goals['home'] is not None else -1
        goles_visita = goals['away'] if goals['away'] is not None else -1
        resultado = 'E'
        if goles_local > goles_visita:
            resultado = 'L'
        elif goles_local < goles_visita:
            resultado = 'V'

        cursor.execute('''
            INSERT INTO partidos (fecha, equipo_local, equipo_visita, goles_local, goles_visita, liga, resultado, clima, lesionados, cuota_local, cuota_visita, acierto)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            fecha,
            local,
            visita,
            goles_local,
            goles_visita,
            league['name'],
            resultado,
            '',
            '',
            0.0,
            0.0,
            None
        ))

    conn.commit()
    print(f"✅ Partidos insertados: {len(partidos)}")
else:
    print("❌ Error al conectar con la API:", response.status_code)

conn.close()
