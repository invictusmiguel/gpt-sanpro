@echo off
setlocal enabledelayedexpansion

:: Activar entorno virtual
echo [INFO] Activando entorno virtual...
call bet365_env\Scripts\activate

:: Ejecutar evaluación
echo [INFO] Ejecutando evaluación de rendimiento...
python scripts\evaluar_parleys.py

:: Mostrar fin
echo [OK] Evaluación completada.
pause
endlocal
