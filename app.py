from datetime import datetime
from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)  # 👈 Primero inicializamos Flask

# 👇 Luego cargamos el modelo
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
        <li><b><a href="https://api-mario.onrender.com/predict?value=LETRA" target="_blank">/predict?value=LETRA</a></b> → Devuelve la posición de la letra en el abecedario</li>
        <li><b><a href="https://api-mario.onrender.com/tipo?value=LETRA" target="_blank">/tipo?value=LETRA</a></b> → Indica si la letra es vocal o consonante</li>
        <li><b><a href="https://api-mario.onrender.com/fecha?value=2025-04-22" target="_blank">/fecha?value=YYYY-MM-DD</a></b> → Devuelve el día de la semana de esa fecha</li>
        <li><b><a href="https://api-mario.onrender.com/modelo?release_year=2021&duration=1&rating=TV-PG" target="_blank">/modelo?release_year=2021&duration=1&rating=TV-PG</a></b> → Usa el modelo para predecir si es Movie o TV Show</li>
        <li><b><a href="https://api-mario.onrender.com/hello" target="_blank">/hello</a></b> → Endpoint extra para redespliegue</li>
    </ul>
    """


@app.route("/modelo")
def modelo():
    try:
        # Recibimos los parámetros por GET
        release_year = int(request.args.get("release_year"))
        duration = int(request.args.get("duration"))
        rating = request.args.get("rating")

        # Codificamos el rating
        rating_encoded = rating_encoder.transform([rating])[0]

        # Creamos el array de entrada
        input_data = np.array([[release_year, duration, rating_encoded]])

        # Predecimos
        prediction = model.predict(input_data)[0]
        resultado = type_encoder.inverse_transform([prediction])[0]

        return jsonify({"prediction": resultado})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/predict")
def predict():
    letra = request.args.get("value", "").lower()

    if len(letra) != 1 or not letra.isalpha():
        return jsonify({"error": "Debes enviar solo UNA letra del abecedario."})

    posicion = ord(letra) - ord('a') + 1
    return jsonify({"position": posicion})


@app.route("/hello")
def hello():
    return "¡Hola mundo desde el endpoint secreto!"


@app.route("/tipo")
def tipo():
    letra = request.args.get("value", "").lower()

    if len(letra) != 1 or not letra.isalpha():
        return jsonify({"error": "Debes enviar solo UNA letra válida."})

    if letra in "aeiou":
        return jsonify({"tipo": "vocal"})
    else:
        return jsonify({"tipo": "consonante"})


@app.route("/fecha")
def fecha():
    valor = request.args.get("value", "")

    try:
        fecha = datetime.strptime(valor, "%Y-%m-%d")
        dias_semana = ["lunes", "martes", "miércoles",
                       "jueves", "viernes", "sábado", "domingo"]
        dia = dias_semana[fecha.weekday()]
        return jsonify({"dia": dia})
    except ValueError:
        return jsonify({"error": "Formato incorrecto. Usa YYYY-MM-DD"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
