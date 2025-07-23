"""
Script para entrenar y guardar el modelo de clasificación de vinos
Basado en el notebook Wine_multiclass_classification__97_5_accuracy.ipynb
"""

import pandas as pd
import numpy as np
import pickle
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, PowerTransformer, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
from imblearn.combine import SMOTEENN
import os

warnings.filterwarnings("ignore")

def load_and_prepare_data():
    """Cargar y preparar los datos del vino"""
    print("🍷 Cargando datos del vino...")
    
    # Cargar el dataset
    df = pd.read_csv("winequality-red.csv")
    print(f"✅ Dataset cargado: {df.shape}")
    
    # Eliminar duplicados
    initial_shape = df.shape[0]
    df = df.drop_duplicates(keep="first")
    print(f"📊 Duplicados eliminados: {initial_shape - df.shape[0]}")
    
    # Separar características y target
    X = df.iloc[:, :-1]  # Todas las columnas excepto 'quality'
    y = df["quality"]
    
    print(f"📈 Características: {X.shape[1]}")
    print(f"🎯 Clases únicas: {sorted(y.unique())}")
    
    return X, y

def balance_and_encode_data(X, y):
    """Balancear datos y codificar etiquetas"""
    print("⚖️  Balanceando datos...")
    
    # Balancear usando SMOTEENN
    smoteenn = SMOTEENN(random_state=42)
    X_balanced, y_balanced = smoteenn.fit_resample(X, y)
    
    print(f"📊 Datos después del balanceado: {X_balanced.shape}")
    
    # Codificar etiquetas para XGBoost (0 a n-1)
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_balanced)
    
    print("🔄 Mapeo de clases:")
    for original, encoded in zip(label_encoder.classes_, range(len(label_encoder.classes_))):
        print(f"   Calidad {original} -> {encoded}")
    
    return X_balanced, y_encoded, label_encoder

def preprocess_features(X_train, X_test):
    """Preprocesar características: transformar asimétricas y escalar"""
    print("🔧 Preprocesando características...")
    
    # Identificar columnas asimétricas (skew > 0.75)
    skew_limit = 0.75
    skew_vals = X_train.skew()
    skewed_cols = skew_vals[abs(skew_vals) > skew_limit].index.tolist()
    
    print(f"📊 Columnas asimétricas detectadas: {len(skewed_cols)}")
    print(f"   {skewed_cols}")
    
    # Aplicar PowerTransformer para corregir asimetría
    power_transformer = PowerTransformer(standardize=False)
    if skewed_cols:
        X_train[skewed_cols] = power_transformer.fit_transform(X_train[skewed_cols])
        X_test[skewed_cols] = power_transformer.transform(X_test[skewed_cols])
        print("✅ Transformación de asimetría aplicada")
    
    # Escalar todas las características
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("✅ Escalado MinMax aplicado")
    
    return X_train_scaled, X_test_scaled, scaler, power_transformer

def train_model(X_train, y_train, X_test, y_test):
    """Entrenar el modelo XGBoost"""
    print("🚀 Entrenando modelo XGBoost...")
    
    # Configurar XGBoost
    model = XGBClassifier(
        n_estimators=500,
        learning_rate=0.1,
        max_depth=6,
        random_state=42,
        eval_metric='mlogloss'
    )
    
    # Entrenar
    model.fit(X_train, y_train)
    
    # Evaluar
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"🎯 Accuracy del modelo: {accuracy:.4f}")
    print("\n📊 Reporte de clasificación:")
    print(classification_report(y_test, y_pred))
    
    return model, accuracy

def save_model_and_scaler(model, scaler, label_encoder, accuracy):
    """Guardar modelo y scaler en archivos pickle"""
    print("💾 Guardando modelo y componentes...")
    
    # Crear directorio static si no existe
    os.makedirs("static", exist_ok=True)
    
    # Guardar modelo
    with open("static/wine_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("✅ Modelo guardado: static/wine_model.pkl")
    
    # Guardar scaler
    with open("static/wine_scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    print("✅ Scaler guardado: static/wine_scaler.pkl")
    
    # Guardar información del modelo
    model_info = {
        'accuracy': accuracy,
        'model_type': 'XGBoost',
        'features': 11,
        'classes': 6,
        'quality_mapping': {0: 3, 1: 4, 2: 5, 3: 6, 4: 7, 5: 8}
    }
    
    with open("static/model_info.pkl", "wb") as f:
        pickle.dump(model_info, f)
    print("✅ Información del modelo guardada: static/model_info.pkl")

def verify_model():
    """Verificar que el modelo guardado funciona correctamente"""
    print("🔍 Verificando modelo guardado...")
    
    try:
        # Cargar modelo y scaler
        model = pickle.load(open("static/wine_model.pkl", "rb"))
        scaler = pickle.load(open("static/wine_scaler.pkl", "rb"))
        
        # Datos de ejemplo para prueba
        example_data = pd.DataFrame({
            'fixed acidity': [7.4],
            'volatile acidity': [0.7],
            'citric acid': [0.0],
            'residual sugar': [1.9],
            'chlorides': [0.076],
            'free sulfur dioxide': [11.0],
            'total sulfur dioxide': [34.0],
            'density': [0.9978],
            'pH': [3.51],
            'sulphates': [0.56],
            'alcohol': [9.4]
        })
        
        # Hacer predicción
        scaled_data = scaler.transform(example_data)
        prediction = model.predict(scaled_data)
        proba = model.predict_proba(scaled_data)
        
        quality_mapping = {0: 3, 1: 4, 2: 5, 3: 6, 4: 7, 5: 8}
        predicted_quality = quality_mapping[prediction[0]]
        confidence = max(proba[0]) * 100
        
        print(f"✅ Prueba exitosa!")
        print(f"   Calidad predicha: {predicted_quality}")
        print(f"   Confianza: {confidence:.1f}%")
        
    except Exception as e:
        print(f"❌ Error en la verificación: {e}")

def main():
    """Función principal"""
    print("🍷 Iniciando entrenamiento del modelo de clasificación de vinos")
    print("=" * 60)
    
    try:
        # 1. Cargar y preparar datos
        X, y = load_and_prepare_data()
        
        # 2. Balancear y codificar
        X_balanced, y_encoded, label_encoder = balance_and_encode_data(X, y)
        
        # 3. Dividir en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X_balanced, y_encoded, test_size=0.2, random_state=42
        )
        print(f"📊 División de datos: Train {X_train.shape}, Test {X_test.shape}")
        
        # 4. Preprocesar características
        X_train_processed, X_test_processed, scaler, power_transformer = preprocess_features(
            X_train.copy(), X_test.copy()
        )
        
        # 5. Entrenar modelo
        model, accuracy = train_model(X_train_processed, y_train, X_test_processed, y_test)
        
        # 6. Guardar modelo y componentes
        save_model_and_scaler(model, scaler, label_encoder, accuracy)
        
        # 7. Verificar modelo
        verify_model()
        
        print("\n" + "=" * 60)
        print("🎉 ¡Entrenamiento completado exitosamente!")
        print(f"🎯 Accuracy final: {accuracy:.4f}")
        print("📁 Archivos generados:")
        print("   - static/wine_model.pkl")
        print("   - static/wine_scaler.pkl")
        print("   - static/model_info.pkl")
        print("\n🚀 Ahora puede ejecutar la aplicación web con: python app_wine.py")
        
    except Exception as e:
        print(f"❌ Error durante el entrenamiento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
