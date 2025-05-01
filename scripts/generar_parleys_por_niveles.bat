@echo off
echo ================================
echo 🧠 Ejecutando Parleys por Niveles
echo ================================
cd /d %~dp0

python generar_parleys_por_niveles.py

echo ✅ Script completado.
pause
