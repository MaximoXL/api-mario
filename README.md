#  API de Letras, Fechas y Clasificación de Contenidos

Bienvenido a esta API desarrollada con **Flask** y **Machine Learning**, capaz de:

- Decir la **posición de una letra** en el abecedario.
- Clasificar si una letra es **vocal o consonante**.
- Decir el **día de la semana** a partir de una fecha.
- Predecir si un contenido es una **película o serie** usando un modelo de Machine Learning.

---
# API Mario

Este proyecto es una API inspirada en el universo de Mario, desarrollada con Python y FastAPI.

##  Requisitos

Antes de ejecutar este proyecto, asegúrate de tener instaladas las siguientes herramientas:

- **Python 3.10+**  
- **Visual Studio Code** (recomendado como entorno de desarrollo)
- **Git** (para clonar el repositorio)

## API desplegada en Render

Puedes probar la API directamente desde tu navegador:

🔗 [https://api-mario-4ek4.onrender.com](https://api-mario-4ek4.onrender.com)

---

## 📌 Endpoints disponibles

| Endpoint | Descripción | Ejemplo |
|----------|-------------|---------|
| `/predict?value=LETRA` | Devuelve la posición de la letra en el abecedario | `/predict?value=a` |
| `/tipo?value=LETRA` | Indica si es vocal o consonante | `/tipo?value=e` |
| `/fecha?value=YYYY-MM-DD` | Devuelve el día de la semana de esa fecha | `/fecha?value=2025-04-22` |
| `/modelo?release_year=YYYY&duration=N&rating=RATING` | Usa ML para predecir si es película o serie | `/modelo?release_year=2017&duration=1&rating=TV-MA` |
| `/hello` | Endpoint de prueba | `/hello` |

---

## 🎬 Variables del modelo (`/modelo`)

El modelo predice si un contenido es una **película** o una **serie (TV Show)** según 3 variables:

1. **`release_year`** → Año de lanzamiento  
   - Ejemplos: `2020`, `2015`, `2019`

2. **`duration`** → Duración en minutos (película) o número de temporadas (serie)  
   - Ejemplos: `90`, `120`, `1`, `2`

3. **`rating`** → Clasificación por edad (**IMPORTANTE**)  
   - Puedes probar con alguno de estos valores:
     - `G` (para todos los públicos)
     - `PG` (supervisión de padres)
     - `PG-13` (mayores de 13)
     - `R` (mayores de 17)
     - `TV-Y` (infantil)
     - `TV-Y7` (mayores de 7)
     - `TV-G`, `TV-PG`, `TV-14`, `TV-MA` (televisión por edad)

**Ejemplo que predice una película**:
```
/modelo?release_year=2019&duration=100&rating=PG
```

**Ejemplo que predice una serie**:
```
/modelo?release_year=2017&duration=1&rating=TV-MA
```


## Cómo desplegar esta API en Render (paso a paso)

1. **Sube tu código a un repositorio de GitHub** (asegúrate de incluir `app.py`, `.pkl`, `Procfile`, `requirements.txt`)
2. Entra a [https://render.com](https://render.com)
3. Crea una cuenta o inicia sesión
4. Haz clic en **"New Web Service"**
5. Elige **"Deploy from GitHub"**
6. Autoriza el acceso y selecciona tu repositorio
7. Configura:
   - **Name**: lo que tú quieras
   - **Runtime**: Python
   - **Build Command**: *(déjalo en blanco o usa `pip install -r requirements.txt`)*
   - **Start Command**: Render lo leerá del `Procfile` (`gunicorn app:app`)
8. Haz clic en **"Create Web Service"**
9. Espera unos segundos y tendrás tu API lista

---

## Archivos importantes

- `app.py` → Código principal de la API
- `train_model.py` → Entrena el modelo
- `model.pkl` → Modelo entrenado
- `rating_encoder.pkl`, `type_encoder.pkl` → Codificadores
- `Procfile` → Configura el arranque en Render
- `requirements.txt` → Lista de librerías necesarias

---

## Requisitos locales (opcional)

Si quieres ejecutarlo en tu PC:

```bash
pip install -r requirements.txt
python app.py
```

---

## Autor

**Mario Tena Rufo**