@echo off
echo ================================
echo 🧠 Ejecutando Módulo 13 - SAMPRO
echo ================================
cd /d %~dp0

echo ▶️ 1. Obteniendo cuotas desde TheOddsAPI...
python fetch_cuotas_theoddsapi.py

echo ▶️ 2. Simulando clima para los partidos...
python fetch_clima_partido.py

echo ▶️ 3. Generando boletín diario (pitchers y lesiones)...
python scrape_pitchers_y_lesiones.py

echo ▶️ 4. Integrando datos en cuotas_diarias.json...
python actualizar_cuotas_diarias.py

echo ▶️ 5. Generando parleys del día...
python auto_parley_update.py

echo ================================
echo ✅ Proceso COMPLETADO bro 💥
echo Revisa:
echo  - data/cuotas_diarias.json
echo  - data/parleys_generados.json
echo  - logs/*.csv
pause
