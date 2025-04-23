import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pickle

# Leemos el archivo CSV
df = pd.read_csv("amazon_prime_titles.csv")

# Eliminamos duplicados
df.drop_duplicates(inplace=True)

# Seleccionamos las columnas con las que trabajaremos y quitamos valores nulos
df = df[["type", "release_year", "duration", "rating"]].dropna()

# Extraemos el número de duración desde la columna 'duration'
df["duration_num"] = df["duration"].str.extract(r"(\d+)").astype(int)

# Transformamos la columna 'rating' como número
rating_encoder = LabelEncoder()
df["rating_encoded"] = rating_encoder.fit_transform(df["rating"])

# Codificamos la variable 'type' (la que queremos predecir)
type_encoder = LabelEncoder()
y = type_encoder.fit_transform(df["type"])  # Movie = 1, TV Show = 0

# Estas son las columnas que usará el modelo como entrada
X = df[["release_year", "duration_num", "rating_encoded"]]

# Dividimos los datos en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Entrenamos el modelo
modelo = RandomForestClassifier()
modelo.fit(X_train, y_train)

# Comprobamos qué tan bien funciona
y_pred = modelo.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Precisión del modelo: {accuracy * 100:.2f}%")

# Guardamos el modelo entrenado
with open("model.pkl", "wb") as f:
    pickle.dump(modelo, f)

# Guardamos el codificador del rating
with open("rating_encoder.pkl", "wb") as f:
    pickle.dump(rating_encoder, f)

# Guardamos el codificador del resultado (Movie / TV Show)
with open("type_encoder.pkl", "wb") as f:
    pickle.dump(type_encoder, f)

print("✅ Modelo y codificadores guardados correctamente.")
