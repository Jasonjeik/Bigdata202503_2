# DistilBERT Model Setup for Production

## ⚠️ IMPORTANT: Git LFS Required

El modelo DistilBERT fine-tuned (256MB) se almacena usando Git LFS (Large File Storage).

### Instalación y Descarga de Pesos

Antes de ejecutar la aplicación en un entorno nuevo, debes descargar los pesos reales:

```bash
# 1. Instalar Git LFS (si no está instalado)
git lfs install

# 2. Descargar pesos de DistilBERT
git lfs pull --include="api/models/distilbert_final/model.safetensors"

# 3. Verificar descarga (debe mostrar ~256MB)
ls -lh api/models/distilbert_final/model.safetensors
```

### Verificación

Si ves un archivo muy pequeño (<1KB), es un pointer de LFS, no los pesos reales:

```bash
# Archivo pointer (incorrecto): ~134 bytes
# Archivo real (correcto): ~256 MB
```

### En Streamlit Cloud

Streamlit Cloud ejecuta `git lfs pull` automáticamente si Git LFS está configurado en el repositorio. Si el modelo no carga:

1. Verifica que `.gitattributes` incluye: `*.safetensors filter=lfs diff=lfs merge=lfs -text`
2. Reinicia el deployment para forzar descarga de LFS

### Comportamiento de Fallback

Si DistilBERT no está disponible (LFS pointer sin descargar), la app automáticamente:
- Muestra advertencia: "⚠ DistilBERT no disponible, se usarán fallbacks"
- Usa LSTM, Logistic Regression o Random Forest como respaldo
- Opcionalmente carga modelo público `distilbert-base-uncased-finetuned-sst-2-english`

### Test de Inferencia

```bash
# Ejecutar test para verificar que DistilBERT carga correctamente
python3 test_quick_inference.py
```

Debe mostrar:
```
✓ DistilBERT local cargado
Model type: local_finetuned
Confidence: ~99% (para frases positivas claras)
```

---

**Archivo creado:** 2025-11-22  
**Último commit verificado:** Inferencia local con pesos reales funcionando correctamente
