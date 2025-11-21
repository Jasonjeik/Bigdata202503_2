# Bigdata202503_2 - Análisis de Sentimiento de Comentarios de Películas

## 📚 Propósito Educativo

**Aplicación de demostración estudiantil - Sin propósito comercial**

Esta aplicación ha sido desarrollada exclusivamente con fines educativos y de demostración para el curso de Big Data 2025-03. No tiene ningún propósito comercial ni está destinada a su uso en producción.

## 📝 Descripción

Aplicación para análisis de sentimiento de comentarios de películas utilizando técnicas de procesamiento de lenguaje natural (NLP). La aplicación permite analizar si un comentario sobre una película es positivo, negativo o neutral.

## 🚀 Características

- Análisis de sentimiento utilizando TextBlob (optimizado para inglés)
- Interfaz de línea de comandos (CLI) simple en español
- Datos de ejemplo para demostración
- Código educativo con comentarios explicativos
- Detección de polaridad y subjetividad

## 📦 Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## 💻 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Jasonjeik/Bigdata202503_2.git
cd Bigdata202503_2

# Instalar dependencias
pip install -r requirements.txt
```

## 🎯 Uso

```bash
# Analizar un comentario (en inglés para mejor precisión)
python sentiment_analyzer.py "This movie is excellent"

# Analizar datos de ejemplo
python sentiment_analyzer.py --demo

# Ver ayuda
python sentiment_analyzer.py --help
```

## 📖 Ejemplos

```bash
# Comentario positivo
python sentiment_analyzer.py "I loved the movie, incredible performances"

# Comentario negativo
python sentiment_analyzer.py "Very boring, I don't recommend it"

# Comentario neutral
python sentiment_analyzer.py "The movie is okay, nothing special"
```

## 📝 Nota sobre el Idioma

Para fines educativos, este proyecto utiliza TextBlob que está optimizado para análisis de sentimiento en inglés. La interfaz y documentación están en español para facilitar el aprendizaje, pero los comentarios a analizar deben estar preferentemente en inglés para obtener mejores resultados.

## ⚠️ Disclaimer

Este proyecto es únicamente para propósitos educativos y de aprendizaje. No debe ser utilizado en entornos de producción ni con fines comerciales. El código y los modelos están simplificados para facilitar el aprendizaje.

## 📄 Licencia

Este proyecto es material educativo y está disponible para uso académico únicamente.
