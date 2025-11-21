# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

## [1.0.0] - 2025-11-21

### Creación Inicial

**Aplicación de Demostración Estudiantil - Sin Propósito Comercial**

Esta es la primera versión del analizador de sentimiento de comentarios de películas para el curso Big Data 2025-03.

#### ✨ Características Añadidas

- **Analizador de Sentimientos**
  - Análisis utilizando TextBlob (optimizado para inglés)
  - Cálculo de polaridad (-1 a +1)
  - Cálculo de subjetividad (0 a 1)
  - Clasificación en POSITIVO, NEGATIVO o NEUTRAL

- **Interfaz CLI**
  - Modo demostración con ejemplos pre-cargados
  - Análisis de comentarios individuales
  - Modo de análisis por lotes (batch)
  - Salida formateada con colores
  - Sistema de ayuda integrado

- **Documentación**
  - README.md completo
  - QUICKSTART.md para inicio rápido
  - CONTRIBUTING.md para contribuciones
  - LICENSE educativo
  - Comentarios explicativos en el código

- **Ejemplos y Datos**
  - sample_data.txt con comentarios de ejemplo
  - example_usage.py con ejemplos programáticos
  - Comentarios de demostración integrados

- **Configuración del Proyecto**
  - requirements.txt con dependencias mínimas
  - .gitignore para Python
  - Estructura de proyecto educativa clara

#### 🎓 Propósito Educativo

Esta aplicación fue creada exclusivamente para:
- Demostración en el curso Big Data 2025-03
- Aprendizaje de procesamiento de lenguaje natural (NLP)
- Práctica con análisis de sentimiento
- Ejemplo de desarrollo de aplicaciones CLI en Python

#### ⚠️ Importante

- **NO** tiene propósito comercial
- **NO** debe usarse en producción
- Es un proyecto **simplificado** para fines educativos
- Optimizado para inglés (limitación de TextBlob)

#### 📦 Dependencias

- textblob==0.17.1
- colorama==0.4.6
- nltk>=3.1 (dependencia de textblob)

#### 🧪 Probado con

- Python 3.12
- Ubuntu Linux
- Comentarios en inglés

---

## Notas de Versión

Este changelog sigue el formato de [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

### Tipos de Cambios
- **Añadido** para nuevas funcionalidades
- **Cambiado** para cambios en funcionalidad existente
- **Obsoleto** para funcionalidades que serán eliminadas
- **Eliminado** para funcionalidades eliminadas
- **Corregido** para corrección de bugs
- **Seguridad** para vulnerabilidades

---

**Recordatorio:** Esta es una aplicación educativa sin propósito comercial.
