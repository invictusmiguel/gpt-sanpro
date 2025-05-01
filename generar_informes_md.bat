@echo off
setlocal enabledelayedexpansion

:: Activar entorno virtual
echo [INFO] Activando entorno virtual...
call bet365_env\Scripts\activate

:: Crear carpeta docs si no existe
if not exist docs (
    mkdir docs
)

:: Generar informe 13.3
echo [INFO] Generando informe M13.3...
python -c "import shutil; shutil.copyfile('scripts/README_m13_3_generador_niveles.md', 'docs/informe_modulo_13.3_generador_por_niveles.md')"

:: Generar informe 13.4
echo [INFO] Generando informe M13.4...
python -c "import shutil; shutil.copyfile('scripts/README_m13_4_evaluacion_predictiva.md', 'docs/informe_modulo_13.4_evaluacion_predictiva.md')"

:: Confirmar final
echo [OK] Todos los informes .md fueron generados o actualizados.
pause
endlocal
