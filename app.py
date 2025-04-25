# importamos las librerías
from datetime import datetime  # Para trabajar fechas
from flask import Flask, request  # Para crear la API
import pickle  # para cargar el modelo de ML
import numpy as np  # para trabajar con arrays

# creamos la app de Flask
app = Flask(__name__)

# cargamos el modelo de machine learning que entrenamos previamente
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
# cargamos el codificador para la columna 'rating'
with open("rating_encoder.pkl", "rb") as f:
    rating_encoder = pickle.load(f)
# cargamos el codificador para el resultado (Movie o TV Show)
with open("type_encoder.pkl", "rb") as f:
    type_encoder = pickle.load(f)

# Página principal de la API (lo primero que se ve al entrar)


@app.route("/")
def home():
    return """
    <h1>API de Letras, Fechas y Machine Learning</h1>
    <p>Bienvenido a tu API. Aquí tienes los endpoints disponibles:</p>
    <ul>
        <li><a href="/predict?value=A">/predict?value=LETRA</a> → Devuelve la posición de la letra en el abecedario</li>
        <li><a href="/tipo?value=A">/tipo?value=LETRA</a> → Indica si la letra es vocal o consonante</li>
        <li><a href="/fecha?value=2025-04-24">/fecha?value=YYYY-MM-DD</a> → Devuelve el día de la semana de esa fecha</li>
        <li><a href="/modelo?release_year=2021&duration=100&rating=TV-PG">/modelo?release_year=YYYY&duration=NUM&rating=CLASIFICACION</a> → Usa el modelo para predecir si es Movie o TV Show</li>
        <li><a href="/hello">/hello</a> → Endpoint extra para redespliegue</li>
    </ul>
    """

# Devuelve la posición de una letra en el abecedario


@app.route("/predict")
def predict():
    # Tomamos la letra enviada en la URL
    letra = request.args.get("value", "").lower()
    if len(letra) != 1 or not letra.isalpha():  # Comprobamos que sea solo UNA letra
        return "<h3>❌ Error</h3><p>Debes enviar solo UNA letra del abecedario.</p>"
    # Calculamos su posición usando el código ASCII
    posicion = ord(letra) - ord('a') + 1
    return f"<h3>✅ Resultado</h3><p>La letra <strong>{letra.upper()}</strong> está en la posición <strong>{posicion}</strong> del abecedario.</p>"

# dice si una letra es vocal o consonante


@app.route("/tipo")
def tipo():
    # Tomamos la letra enviada en la URL
    letra = request.args.get("value", "").lower()
    if len(letra) != 1 or not letra.isalpha():  # Comprobamos que sea solo UNA letra
        return "<h3>❌ Error</h3><p>Debes enviar solo UNA letra válida.</p>"
    # Comprobamos si está en la lista de vocales
    tipo = "vocal" if letra in "aeiou" else "consonante"
    return f"<h3>✅ Resultado</h3><p>La letra <strong>{letra.upper()}</strong> es una <strong>{tipo}</strong>.</p>"

# dice qué día de la semana corresponde a una fecha


@app.route("/fecha")
def fecha():
    valor = request.args.get("value", "")
    try:
        # Convertimos el string en una fecha
        fecha_obj = datetime.strptime(valor, "%Y-%m-%d")
        dias = ["lunes", "martes", "miércoles",
                "jueves", "viernes", "sábado", "domingo"]
        # Obtenemos el día de la semana (número) y lo pasamos a texto
        dia = dias[fecha_obj.weekday()]
        return f"<h3>📅 Fecha</h3><p>El <strong>{valor}</strong> fue un <strong>{dia}</strong>.</p>"
    except ValueError:
        return "<h3>❌ Error</h3><p>Formato incorrecto. Usa YYYY-MM-DD</p>"

# Usa el modelo para predecir si es una película o una serie


@app.route("/modelo")
def modelo():
    try:
        # Recogemos los datos desde la URL
        release_year = int(request.args.get("release_year"))
        duration = int(request.args.get("duration"))
        rating = request.args.get("rating")
        # Convertimos el rating a un número usando el codificador(tranformar texto a número)
        rating_encoded = rating_encoder.transform([rating])[0]
        # Preparamos los datos para pasarlos al modelo
        input_data = np.array([[release_year, duration, rating_encoded]])
        # Hacemos la predicción
        prediction = model.predict(input_data)[0]
        # Volvemos a convertir el resultado en texto ("Movie" o "TV Show")
        resultado = type_encoder.inverse_transform([prediction])[0]

        return f"<h3>🎬 Predicción</h3><p>Con esos datos, el modelo predice que es un <strong>{resultado}</strong>.</p>"

    except Exception as e:
        return f"<h3>❌ Error</h3><p>{str(e)}</p>"

# Endpoint de prueba para verificar que la app funciona


@app.route("/hello")
def hello():
    return "<h3>👋 ¡Hola mundo desde el endpoint secreto! :( </h3>"


# Esto sirve solo cuando ejecutamos el archivo localmente, no para render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
