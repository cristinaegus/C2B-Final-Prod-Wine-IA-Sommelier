import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder

def train_random_forest_model():
    """Entrenar modelo Random Forest con 4 características"""
    print("🌲 Entrenando modelo RandomForestClassifier con 4 características...")
    DATASET_PATH = "static/dataset_vinos_combinado_ultra_limpio_20250717_122604.csv"
    df = pd.read_csv(DATASET_PATH)
    features = ["num_reviews", "precio_eur", "rating", "tipo_vino"]
    target = "categoria_calidad"
    df = df.dropna(subset=features + [target])
    le_tipo_vino = LabelEncoder()
    df["tipo_vino_encoded"] = le_tipo_vino.fit_transform(df["tipo_vino"].astype(str))
    le_calidad = LabelEncoder()
    df["calidad_encoded"] = le_calidad.fit_transform(df[target].astype(str))
    X = df[["num_reviews", "precio_eur", "rating", "tipo_vino_encoded"]].values
    y = df["calidad_encoded"].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    with open("static/wine_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("static/wine_scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    with open("static/label_encoder_tipo_vino.pkl", "wb") as f:
        pickle.dump(le_tipo_vino, f)
    with open("static/label_encoder_calidad.pkl", "wb") as f:
        pickle.dump(le_calidad, f)
    print("✅ Modelo y scaler guardados en static/")
    print(f"Clases calidad: {le_calidad.classes_}")
    print(f"Clases tipo_vino: {le_tipo_vino.classes_}")

if __name__ == "__main__":
    train_random_forest_model()

    # Ejemplo de predicción con el modelo entrenado
    # Cargar modelo y scaler
    with open("static/wine_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("static/wine_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("static/label_encoder_tipo_vino.pkl", "rb") as f:
        le_tipo_vino = pickle.load(f)
    with open("static/label_encoder_calidad.pkl", "rb") as f:
        le_calidad = pickle.load(f)

    # Ejemplo: predicción para un vino blanco
    ejemplo = {
        "num_reviews": 500,
        "precio_eur": 20.0,
        "rating": 4.2,
        "tipo_vino": "blanco"
    }
    # Normalizar tipo_vino para coincidir con el encoder
    tipo_vino_normalizado = ejemplo["tipo_vino"].capitalize()
    tipo_vino_encoded = le_tipo_vino.transform([tipo_vino_normalizado])[0]
    X_ejemplo = np.array([[ejemplo["num_reviews"], ejemplo["precio_eur"], ejemplo["rating"], tipo_vino_encoded]])
    X_ejemplo_scaled = scaler.transform(X_ejemplo)
    pred = model.predict(X_ejemplo_scaled)[0]
    calidad_predicha = le_calidad.inverse_transform([pred])[0]
    print(f"\n🔮 Predicción ejemplo: {calidad_predicha} para vino tipo {tipo_vino_normalizado}")
