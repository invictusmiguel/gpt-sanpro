@echo off
setlocal enabledelayedexpansion

:: Crear carpetas necesarias
if not exist logs (
    mkdir logs
)
if not exist backup_logs (
    mkdir backup_logs
)

:: Timestamp para archivo
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set "FECHA=%%i"
set "LOGFILE=logs\%FECHA%.log"
set "ALIAS_LOG=logs\ultima_ejecucion.log"
set "ZIPFILE=backup_logs\%FECHA%_log.zip"

:: Validar archivo de picks
IF NOT EXIST data\picks_validados.json (
    echo [ERROR] No se encuentra data\picks_validados.json > %LOGFILE%
    echo [ERROR] No se encuentra data\picks_validados.json
    start notepad %LOGFILE%
    exit /b 1
)

echo [OK] Archivo de picks encontrado. > %LOGFILE%

:: Activar entorno virtual
echo [INFO] Activando entorno virtual... >> %LOGFILE%
call bet365_env\Scripts\activate >> %LOGFILE% 2>&1

:: Ejecutar generación
echo [INFO] Ejecutando generador de parleys... >> %LOGFILE%
python scripts\generar_parleys_por_niveles.py >> %LOGFILE% 2>&1

:: Ejecutar tests
echo [INFO] Ejecutando tests... >> %LOGFILE%
pytest test_generar_parleys.py >> %LOGFILE% 2>&1
if errorlevel 1 (
    echo [ERROR] Algunos tests fallaron. Revisa el log: %LOGFILE% >> %LOGFILE%
    echo [ERROR] Algunos tests fallaron. Revisa el log: %LOGFILE%
    copy /Y %LOGFILE% %ALIAS_LOG% >nul
    powershell Compress-Archive -Path "%LOGFILE%" -DestinationPath "%ZIPFILE%"
    start notepad %LOGFILE%
    exit /b 1
)

echo [OK] Todo finalizado correctamente. >> %LOGFILE%

:: Guardar ZIP comprimido del log
powershell Compress-Archive -Path "%LOGFILE%" -DestinationPath "%ZIPFILE%"

:: Copiar alias y mostrar
copy /Y %LOGFILE% %ALIAS_LOG% >nul
type %LOGFILE%

endlocal
