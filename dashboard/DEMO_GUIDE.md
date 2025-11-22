# 🎬 Guía de Demostración MovieLover

## Preparación de la Demostración

### Antes de Comenzar
Tu aplicación ahora está configurada para **compartir reseñas entre todas las sesiones** en tiempo real. Todos los participantes verán las mismas reseñas instantáneamente.

### Controles de Administrador

**Contraseña de Admin:** `demo2025`

#### Cómo Acceder:
1. Ve a la barra lateral (sidebar)
2. Busca la sección **"🔐 Admin Controls"**
3. Haz clic para expandir
4. Ingresa la contraseña: `demo2025`
5. Haz clic en **"Unlock Admin"**

#### Funcionalidades de Admin:
- **🗑️ Reset All Reviews**: Limpia todas las reseñas de la base de datos
- **🔒 Lock Admin**: Cierra el modo administrador

---

## Flujo de la Demostración

### 1. Preparación (Antes de la Audiencia)
```bash
# Iniciar la aplicación
streamlit run dashboard/app.py
```

- Activa el modo admin y limpia reseñas anteriores si es necesario
- Verifica que la base de datos esté conectada (indicador en sidebar)

### 2. Durante la Demostración

#### Para los Participantes:
1. Cada participante abre la app en su navegador
2. Navegan a **"Movie Catalog"**
3. Seleccionan una película
4. Escriben su reseña (en cualquier idioma)
5. Califican con estrellas (1-10)
6. Envían su reseña

#### Lo Que Verán en Tiempo Real:
- **Home**: Métricas totales actualizadas
  - Total de reseñas de todos
  - Porcentaje de sentimiento positivo
  - Número de participantes activos
  
- **Live Analytics**: Dashboard compartido
  - Gráficos de sentimiento
  - Timeline de reseñas
  - Distribución de calificaciones
  - Top películas más reseñadas
  - **Toggle "Auto-refresh"**: Refresca automáticamente cada 10 segundos

- **Model Comparison**: Comparación de modelos
  - Predicciones de múltiples modelos
  - Análisis de confianza

### 3. Características Destacadas para Mencionar

#### Multilingüe 🌍
- Los participantes pueden escribir en **cualquier idioma**
- La app detecta automáticamente el idioma
- Traduce al inglés para análisis de sentimiento
- Muestra el idioma original en los analytics

#### Tiempo Real ⚡
- Las reseñas aparecen instantáneamente para todos
- Auto-refresh opcional en Live Analytics
- Contador de participantes activos

#### Múltiples Modelos de IA 🤖
- **DistilBERT** (Recomendado) - Transformer de última generación
- **LSTM Deep Learning** - Red neuronal recurrente
- **Logistic Regression** - ML clásico
- **Random Forest** - Ensemble learning

#### Base de Datos en la Nube ☁️
- MongoDB Atlas (conexión en tiempo real)
- Azure integration

### 4. Puntos de Interacción con la Audiencia

**Preguntas para Hacer:**
- "¿Quién ha visto [película X]? ¡Escribe tu reseña ahora!"
- "Vamos a ver cómo el sentimiento cambia con más reseñas"
- "Comparen: ¿Los 4 modelos están de acuerdo?"

**Actividades Sugeridas:**
1. **Batalla de Películas**: Divide a la audiencia, cada grupo reseña una película diferente
2. **Test Multilingüe**: Pide reseñas en diferentes idiomas (español, inglés, etc.)
3. **Sentimiento Extremo**: Pide una reseña muy positiva y otra muy negativa de la misma película

### 5. Al Finalizar la Demostración

#### Opción A: Mantener los Datos
- Deja las reseñas para análisis posterior
- Exporta las estadísticas

#### Opción B: Limpiar para la Próxima Demo
1. Activa Admin Mode (contraseña: `demo2025`)
2. Haz clic en **"🗑️ Reset All Reviews"**
3. Confirma que se limpiaron todas las reseñas
4. Cierra Admin Mode

---

## Troubleshooting Rápido

### Si no aparecen las reseñas de otros usuarios:
- ✅ Verifica que "Database Connected" esté en verde (sidebar)
- 🔄 Haz clic en "Refresh Data" en Live Analytics
- 🔁 Activa "Auto-refresh" toggle

### Si la base de datos está desconectada:
- Verifica tu conexión a internet
- Revisa las credenciales en `config.py`
- Reinicia la aplicación

### Si el auto-refresh no funciona:
- Desactiva y vuelve a activar el toggle
- Usa el botón manual "🔄 Refresh Data"

---

## Estadísticas en Tiempo Real

### Sidebar Muestra:
- **Total Movies**: Películas en catálogo
- **Total Reviews (All Users)**: Todas las reseñas de la demo
- **Your Reviews (This Session)**: Reseñas de tu navegador específico
- **Active Participants**: Número de usuarios únicos que han participado

### Home Dashboard Muestra:
- **Movies Available**: Total en DB
- **Total Reviews**: Con delta de esta sesión
- **Positive Sentiment**: Porcentaje global
- **Active Models**: Modelos disponibles (4)
- **Active Participants**: Usuarios únicos

---

## Configuración Técnica

### Contraseña de Admin
Para cambiar la contraseña de admin, edita en `app.py`:
```python
if admin_password == "demo2025":  # Cambia "demo2025" aquí
```

### Tiempo de Auto-Refresh
Para cambiar el intervalo de auto-refresh (actualmente 10 segundos):
```python
time.sleep(10)  # Cambia el número de segundos
```

---

## Comandos Útiles

### Iniciar la App
```bash
cd /workspaces/Bigdata202503_2
streamlit run dashboard/app.py
```

### Iniciar con Puerto Específico
```bash
streamlit run dashboard/app.py --server.port 8501
```

### Ver Logs
La app imprime logs en la consola donde la ejecutaste

---

## Recursos Adicionales

- **Documentación completa**: Ver `README.md` en `/dashboard`
- **Configuración de API**: Ver `OMDB_API_SETUP.md`
- **Troubleshooting**: Ver `OMDB_TROUBLESHOOTING.md`

---

## Checklist Pre-Demo

- [ ] Base de datos conectada
- [ ] Modelos cargados correctamente
- [ ] Contraseña de admin probada
- [ ] Reset de reseñas anteriores (si aplica)
- [ ] Internet estable
- [ ] URL compartida con participantes (si demo remota)
- [ ] Películas de ejemplo seleccionadas
- [ ] Auto-refresh testeado

---

## Tips para una Demo Exitosa

1. **Empieza con el Home** para mostrar el overview
2. **Ve al Catálogo** y muestra las películas con posters
3. **Haz una reseña de ejemplo** tú mismo primero
4. **Invita a la audiencia** a participar
5. **Cambia a Live Analytics** para ver resultados en tiempo real
6. **Activa Auto-refresh** para efecto "wow"
7. **Muestra Model Comparison** para destacar la IA
8. **Finaliza con Model Architecture** para explicar la tecnología

---

¡Éxito en tu demostración! 🎉
