 Ruta sugerida:
docs/informe_modulo_13.3_generador_por_niveles.md

🧾 Informe Técnico — SAMPRO
Módulo 13.3 — Generador por Niveles
🧠 Objetivo del módulo
Crear un sistema de generación de parleys matemáticamente clasificados por nivel de seguridad usando los picks ya validados en etapas anteriores del sistema SAMPRO.

✅ Actividades realizadas
1. 🛠 Corrección de errores críticos
Error corregido: KeyError: 'ev' que ocurría al intentar acceder a campos no presentes en algunos picks.

Solución aplicada: Cálculo dinámico del valor_esperado (ev) dentro del mismo script, y uso de .get() para evitar errores por ausencia de claves.

2. ♻️ Refactor y organización de funciones
Reestructuración de funciones nivel_2_combinaciones y nivel_3_combinaciones para usar filtros más robustos.

Centralización del cálculo de métricas (cuota total, probabilidad total, EV) en una única función generar_parleys().

3. 🧪 Validaciones (manuales y automáticas)
Se validaron los siguientes criterios:

Test / Validación	Estado
Archivo parleys_por_nivel.json generado	✅
Estructura de niveles (nivel_1/2/3)	✅
Picks con EV y Z-score en Nivel 3	✅
Combinaciones correctas (2 o 3 picks)	✅
Flujo completo sin errores	✅

4. ⚙️ Automatización con script .bat
Se creó un archivo run_todo.bat que:

Ejecuta el generador completo.

Genera los parleys_por_nivel.json.

Almacena logs por ejecución.

Permite trazabilidad futura.

📦 Resultado final generado
Archivo: data/parleys_por_nivel.json

Estructura:

json
Copiar
Editar
{
  "fecha": "2025-05-01",
  "nivel_1": [...],
  "nivel_2": [...],
  "nivel_3": [...]
}
Nivel 1: Picks APTOS sin filtro adicional.

Nivel 2: Picks recomendables (prob ≥ 0.65, EV ≥ 0.80).

Nivel 3: Picks ultra seguros (prob ≥ 0.75, EV ≥ 1.0, z-score ∈ [-1, 1]).

📄 Documentación técnica del módulo
A partir de este módulo, se establece la práctica de generar un informe técnico por cada módulo trabajado, con el objetivo de:

Documentar decisiones y lógica de negocio.

Facilitar auditorías y debugging.

Dejar trazabilidad para nuevos desarrolladores.

Este informe fue guardado como:

bash
Copiar
Editar
docs/informe_modulo_13.3_generador_por_niveles.md
📌 Recomendaciones para el Módulo 13.4
Evaluar rendimiento predictivo: comparar los parleys generados con resultados reales.

Crear reporte de aciertos: aciertos por nivel, ROI, EV real vs esperado.

Dashboard resumen en consola con porcentajes de éxito por tipo de parley.