# ⚾ SAMPRO v2.0 – Sports AI Parley Predictor

**SAMPRO** (Sistema Automatizado de Modelos Predictivos y Resultados de Oportunidad) es una plataforma basada en Flask + IA que permite:

- Generar predicciones deportivas sabermétricas.
- Construir parleys clasificados por nivel de seguridad matemática.
- Evaluar el rendimiento real diario (ROI, aciertos, EV real).
- Conectarse como plugin oficial en ChatGPT.

---

## 🔮 ¿Qué hace SAMPRO?

### ✅ Predicción con IA
Usa modelos entrenados para calcular:
- Diferencial de carreras
- Probabilidad de victoria
- Explicación en lenguaje natural (estilo GPT)

### ✅ Parleys inteligentes
Clasifica combinaciones como:
- Nivel 1: picks válidos
- Nivel 2: picks recomendables (prob ≥ 0.65, EV ≥ 0.80)
- Nivel 3: ultra seguros (prob ≥ 0.75, EV ≥ 1.0, z-score ∈ [-1, 1])

### ✅ Evaluación diaria
Evalúa automáticamente:
- % de éxito por nivel
- ROI estimado vs real
- Rendimiento acumulado

---

## 🔌 Conexión como Plugin de ChatGPT

SAMPRO está preparado para ser usado como plugin personalizado en ChatGPT.

### 📂 Archivos clave:

| Archivo             | Función |
|---------------------|--------|
| `ai-plugin.json`    | Define el plugin GPT |
| `openapi.yaml`      | Documentación de endpoints |
| `app.py`            | API Flask principal |
| `logo.png`          | Logo del plugin (en `/static/`) |
| `legal.html`        | Página legal visible del plugin |

---

## 🚀 Cómo ejecutarlo localmente

```bash
# Instala dependencias
pip install -r requirements.txt

# Ejecuta la app
python app.py
