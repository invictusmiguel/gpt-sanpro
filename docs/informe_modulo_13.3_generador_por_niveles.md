# 🧠 M13.3 – Generador de Parleys por Niveles

Genera combinaciones de picks validados en distintos niveles de confianza, basados en criterios matemáticos como probabilidad, valor esperado y z-score.

---

## 🎯 Objetivo

- Tomar los picks validados (`picks_validados.json`)
- Generar combinaciones por nivel:
  - Nivel 1: todos los picks válidos
  - Nivel 2: picks confiables (prob ≥ 0.65 y EV ≥ 0.80)
  - Nivel 3: picks seguros (prob ≥ 0.75, EV ≥ 1.0, z-score ∈ [-1, 1])
- Calcular EV y Z-Score si faltan
- Guardar resultados en `parleys_por_nivel.json`

---

## 📁 Archivos clave

| Archivo                             | Descripción                                              |
|-------------------------------------|----------------------------------------------------------|
| `scripts/generar_parleys_por_niveles.py` | Lógica de generación por nivel                           |
| `data/picks_validados.json`         | Entrada: picks procesados y validados                    |
| `data/parleys_por_nivel.json`       | Salida: parleys combinados por nivel                     |
| `test_generar_parleys.py`           | Pruebas automáticas de generación                        |
| `run_todo.bat`                      | Ejecuta generación y tests en un clic                    |

---

## 🚀 Ejecución

```bash
python scripts/generar_parleys_por_niveles.py
