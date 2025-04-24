from datetime import datetime
from flask import Flask, request
import pickle
import numpy as np

app = Flask(__name__)

# Cargamos el modelo y codificadores
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("rating_encoder.pkl", "rb") as f:
    rating_encoder = pickle.load(f)

with open("type_encoder.pkl", "rb") as f:
    type_encoder = pickle.load(f)


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


@app.route("/predict")
def predict():
    letra = request.args.get("value", "").lower()
    if len(letra) != 1 or not letra.isalpha():
        return "<h3>❌ Error</h3><p>Debes enviar solo UNA letra del abecedario.</p>"
    posicion = ord(letra) - ord('a') + 1
    return f"<h3>✅ Resultado</h3><p>La letra <strong>{letra.upper()}</strong> está en la posición <strong>{posicion}</strong> del abecedario.</p>"


@app.route("/tipo")
def tipo():
    letra = request.args.get("value", "").lower()
    if len(letra) != 1 or not letra.isalpha():
        return "<h3>❌ Error</h3><p>Debes enviar solo UNA letra válida.</p>"
    tipo = "vocal" if letra in "aeiou" else "consonante"
    return f"<h3>✅ Resultado</h3><p>La letra <strong>{letra.upper()}</strong> es una <strong>{tipo}</strong>.</p>"


@app.route("/fecha")
def fecha():
    valor = request.args.get("value", "")
    try:
        fecha_obj = datetime.strptime(valor, "%Y-%m-%d")
        dias = ["lunes", "martes", "miércoles",
                "jueves", "viernes", "sábado", "domingo"]
        dia = dias[fecha_obj.weekday()]
        return f"<h3>📅 Fecha</h3><p>El <strong>{valor}</strong> fue un <strong>{dia}</strong>.</p>"
    except ValueError:
        return "<h3>❌ Error</h3><p>Formato incorrecto. Usa YYYY-MM-DD</p>"


@app.route("/modelo")
def modelo():
    try:
        release_year = int(request.args.get("release_year"))
        duration = int(request.args.get("duration"))
        rating = request.args.get("rating")

        rating_encoded = rating_encoder.transform([rating])[0]
        input_data = np.array([[release_year, duration, rating_encoded]])
        prediction = model.predict(input_data)[0]
        resultado = type_encoder.inverse_transform([prediction])[0]

        return f"<h3>🎬 Predicción</h3><p>Con esos datos, el modelo predice que es un <strong>{resultado}</strong>.</p>"

    except Exception as e:
        return f"<h3>❌ Error</h3><p>{str(e)}</p>"


@app.route("/hello")
def hello():
    return "<h3>👋 ¡Hola mundo desde el endpoint secreto!</h3>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
