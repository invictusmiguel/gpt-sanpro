# 📊 M13.4 – Evaluación de Rendimiento Predictivo + ROI Real

Este módulo evalúa los parleys generados en cada nivel (1, 2 y 3) comparándolos con los resultados reales del día. Calcula métricas de rendimiento y guarda tanto el resumen diario como un log acumulado.

---

## 🎯 Objetivo

- Comparar cada parley con los resultados reales
- Calcular métricas clave por nivel:
  - ✅ Aciertos
  - ❌ Fallos
  - 📈 Porcentaje de éxito
  - 💰 ROI (Rentabilidad)
  - ⚖️ Valor Esperado Real Promedio (EV real)
- Generar un resumen diario en consola y archivo

---

## 📁 Archivos clave

| Archivo                              | Descripción                                                  |
|--------------------------------------|--------------------------------------------------------------|
| `scripts/evaluar_parleys.py`         | Script principal del módulo                                  |
| `data/resultados_reales.json`        | Entrada con los resultados reales de los eventos             |
| `data/parleys_por_nivel.json`        | Entrada con los parleys generados por nivel                  |
| `data/evaluacion_resultados.json`    | Salida en formato JSON con el resumen de evaluación          |
| `logs/evaluacion_predictiva.csv`     | Log CSV acumulado de cada ejecución                          |
| `test_evaluacion_predictiva.py`      | Pruebas unitarias del módulo                                 |
| `evaluar_todo.bat`                   | Script para ejecutar evaluación con un clic                  |

---

## 🖥️ Ejecución

```bash
python scripts/evaluar_parleys.py
