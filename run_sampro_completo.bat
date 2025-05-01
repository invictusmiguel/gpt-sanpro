@echo off
setlocal enabledelayedexpansion

:: Timestamp para logs y copias
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set "FECHA=%%i"
set "LOGFILE=logs\sampro_%FECHA%.log"
set "ALIAS_LOG=logs\sampro_ultima_ejecucion.log"
set "ZIPFILE=backup_logs\sampro_%FECHA%.zip"

:: Crear carpetas si no existen
if not exist logs mkdir logs
if not exist backup_logs mkdir backup_logs

:: Validar que picks existan
IF NOT EXIST data\picks_validados.json (
    echo [ERROR] Faltan los picks validados. > %LOGFILE%
    echo [ERROR] Faltan los picks validados.
    start notepad %LOGFILE%
    exit /b 1
)

:: Activar entorno
echo [INFO] Activando entorno virtual... >> %LOGFILE%
call bet365_env\Scripts\activate >> %LOGFILE% 2>&1

:: === Módulo 13.3: Generación de parleys ===
echo [INFO] Ejecutando generación de parleys... >> %LOGFILE%
python scripts\generar_parleys_por_niveles.py >> %LOGFILE% 2>&1

:: === Módulo 13.4: Evaluación de rendimiento ===
echo [INFO] Ejecutando evaluación predictiva... >> %LOGFILE%
python scripts\evaluar_parleys.py >> %LOGFILE% 2>&1

:: === Tests ===
echo [INFO] Ejecutando tests... >> %LOGFILE%
pytest test_generar_parleys.py >> %LOGFILE% 2>&1
pytest test_evaluacion_predictiva.py >> %LOGFILE% 2>&1

:: Comprimir log y guardar alias
powershell Compress-Archive -Path "%LOGFILE%" -DestinationPath "%ZIPFILE%"
copy /Y %LOGFILE% %ALIAS_LOG% >nul

:: Mostrar resultados
type %LOGFILE%
echo [OK] Ejecución completa de SAMPRO.
pause
endlocal
