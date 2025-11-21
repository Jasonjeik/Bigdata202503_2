# 🚀 Guía de Inicio Rápido

## Para Estudiantes del Curso Big Data 2025-03

Esta guía te ayudará a comenzar rápidamente con el analizador de sentimientos.

### ⚠️ Recordatorio Importante

Esta es una **aplicación de demostración estudiantil** creada exclusivamente para propósitos educativos. No tiene ningún propósito comercial.

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8 o superior**
  ```bash
  python --version
  ```

- **pip** (gestor de paquetes de Python)
  ```bash
  pip --version
  ```

---

## 🔧 Instalación en 3 Pasos

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/Jasonjeik/Bigdata202503_2.git
cd Bigdata202503_2
```

### Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Descargar Datos de NLTK

```bash
python -m textblob.download_corpora
```

---

## 🎯 Uso Básico

### 1. Modo Demostración (Recomendado para empezar)

Ejecuta el analizador con comentarios de ejemplo:

```bash
python sentiment_analyzer.py --demo
```

Este modo te mostrará:
- 8 comentarios de ejemplo analizados
- Resultados con polaridad y subjetividad
- Estadísticas generales

### 2. Analizar un Comentario Individual

```bash
python sentiment_analyzer.py "This movie is amazing"
```

**Ejemplos:**

```bash
# Comentario positivo
python sentiment_analyzer.py "Excellent movie, highly recommended"

# Comentario negativo  
python sentiment_analyzer.py "Terrible film, waste of time"

# Comentario neutral
python sentiment_analyzer.py "It was okay, nothing special"
```

### 3. Ver Opciones de Ayuda

```bash
python sentiment_analyzer.py --help
```

---

## 💡 Uso Programático

Si quieres usar el analizador en tu propio código Python:

```bash
python example_usage.py
```

O crea tu propio script:

```python
from sentiment_analyzer import SentimentAnalyzer

# Crear analizador
analyzer = SentimentAnalyzer()

# Analizar un comentario
result = analyzer.analyze_sentiment("Great movie!")

# Ver resultado
print(f"Sentimiento: {result['sentiment']}")
print(f"Polaridad: {result['polarity']}")
```

---

## 📊 Entendiendo los Resultados

### Polaridad
- **Rango:** -1.0 (muy negativo) a +1.0 (muy positivo)
- **> 0.1:** Sentimiento POSITIVO
- **< -0.1:** Sentimiento NEGATIVO
- **Entre -0.1 y 0.1:** Sentimiento NEUTRAL

### Subjetividad
- **Rango:** 0.0 (muy objetivo) a 1.0 (muy subjetivo)
- **Valores altos:** Comentario basado en opiniones personales
- **Valores bajos:** Comentario basado en hechos

---

## 🌍 Nota sobre el Idioma

**Importante:** Este analizador funciona mejor con comentarios en **inglés** porque utiliza TextBlob, que está optimizado para ese idioma.

✅ **Recomendado:** `"This movie is excellent"`  
❌ **No óptimo:** `"Esta película es excelente"`

La interfaz y documentación están en español para facilitar el aprendizaje, pero los comentarios a analizar deben estar en inglés.

---

## 🔍 Ejemplos de Uso Práctico

### Ejemplo 1: Analizar Múltiples Comentarios

Crea un archivo `mis_comentarios.txt`:
```
This movie is amazing
Terrible waste of time
Pretty good overall
```

Luego analiza:
```bash
cat mis_comentarios.txt | python sentiment_analyzer.py --batch
```

### Ejemplo 2: Guardar Resultados

```bash
python sentiment_analyzer.py --demo > resultados.txt
```

---

## ❓ Solución de Problemas

### Problema: "ModuleNotFoundError: No module named 'textblob'"

**Solución:** Instala las dependencias
```bash
pip install -r requirements.txt
```

### Problema: "Resource punkt not found"

**Solución:** Descarga los datos de NLTK
```bash
python -m textblob.download_corpora
```

### Problema: Los resultados no son precisos

**Solución:** 
- Asegúrate de usar comentarios en inglés
- Recuerda que es un modelo educativo simplificado
- Los resultados pueden variar según el contexto

---

## 📚 Recursos Adicionales

- **Documentación de TextBlob:** https://textblob.readthedocs.io/
- **Guía de NLP en Python:** https://realpython.com/nltk-nlp-python/

---

## 🤝 Contribuciones

Lee `CONTRIBUTING.md` para más información sobre cómo contribuir a este proyecto educativo.

---

## 📝 Licencia

Este proyecto es material educativo. Ver `LICENSE` para más detalles.

---

**¡Feliz aprendizaje! 🎓**

Si tienes preguntas, contacta a través de los canales del curso Big Data 2025-03.
