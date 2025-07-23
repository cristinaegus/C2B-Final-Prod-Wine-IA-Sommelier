#!/usr/bin/env python3
"""
Script para entrenar el modelo Sommelier con datos de Vivino
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle
import glob
import os

def encontrar_archivo_mas_reciente():
    """Encuentra el archivo CSV más reciente de scraping"""
    archivos = glob.glob('datos_scraping/vivino_scraping_completo_*.csv')
    if not archivos:
        print("❌ No se encontraron archivos de scraping")
        return None
    
    archivo_mas_reciente = max(archivos, key=os.path.getctime)
    print(f"✅ Usando archivo: {archivo_mas_reciente}")
    return archivo_mas_reciente

def cargar_datos():
    """Carga y prepara los datos"""
    archivo = encontrar_archivo_mas_reciente()
    if not archivo:
        return None
    
    df = pd.read_csv(archivo)
    print(f"📊 Datos cargados: {len(df)} vinos")
    print(f"📋 Columnas: {list(df.columns)}")
    return df

def limpiar_datos(df):
    """Limpia y prepara los datos para el entrenamiento"""
    df_clean = df.copy()
    
    # Limpiar columna rating
    def limpiar_rating(rating_str):
        try:
            if isinstance(rating_str, (int, float)):
                return float(rating_str)
            import re
            numeros = re.findall(r'(\d+\.?\d*)', str(rating_str))
            if numeros:
                return float(numeros[0])
            return 4.0
        except:
            return 4.0
    
    df_clean['rating_limpio'] = df_clean['rating'].apply(limpiar_rating)
    
    # Verificar si existe la columna precio_euros o similar
    columnas_precio = [col for col in df_clean.columns if 'precio' in col.lower()]
    if columnas_precio:
        precio_col = columnas_precio[0]
        print(f"✅ Usando columna de precio: {precio_col}")
    else:
        print("❌ No se encontró columna de precio")
        return None
    
    # Crear categorías de calidad basadas en rating
    def categorizar_calidad(rating):
        if rating >= 4.15:
            return 'Excelente'
        elif rating >= 4.10:
            return 'Muy Bueno'
        elif rating >= 4.05:
            return 'Bueno'
        elif rating >= 4.00:
            return 'Regular'
        else:
            return 'Básico'
    
    df_clean['categoria_calidad'] = df_clean['rating_limpio'].apply(categorizar_calidad)
    
    # Características para el modelo
    caracteristicas = []
    
    # Precio
    caracteristicas.append(precio_col)
    
    # Rating limpio
    caracteristicas.append('rating_limpio')
    
    # Año (si existe)
    if 'año' in df_clean.columns:
        caracteristicas.append('año')
    else:
        df_clean['año'] = 2021  # Valor por defecto
        caracteristicas.append('año')
    
    # Posición
    if 'posicion' in df_clean.columns:
        caracteristicas.append('posicion')
    else:
        df_clean['posicion'] = range(1, len(df_clean) + 1)
        caracteristicas.append('posicion')
    
    # Número de reviews
    columnas_reviews = [col for col in df_clean.columns if 'review' in col.lower()]
    if columnas_reviews:
        reviews_col = columnas_reviews[0]
        caracteristicas.append(reviews_col)
    else:
        df_clean['num_reviews'] = 500  # Valor por defecto
        caracteristicas.append('num_reviews')
    
    print(f"✅ Características seleccionadas: {caracteristicas}")
    print(f"✅ Variable objetivo: categoria_calidad")
    
    return df_clean, caracteristicas

def entrenar_modelo(df, caracteristicas):
    """Entrena el modelo Random Forest"""
    
    # Preparar datos
    X = df[caracteristicas].fillna(0)
    y = df['categoria_calidad']
    
    print(f"📊 Forma de X: {X.shape}")
    print(f"📊 Distribución de clases:")
    print(y.value_counts())
    
    # Encoders
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    # Entrenar modelo
    print("🤖 Entrenando Random Forest...")
    modelo = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1
    )
    
    modelo.fit(X_train, y_train)
    
    # Evaluar
    y_pred = modelo.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Precisión del modelo: {accuracy:.2%}")
    print("\n📋 Reporte de clasificación:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
    
    # Importancia de características
    importancias = modelo.feature_importances_
    for i, caracteristica in enumerate(caracteristicas):
        print(f"   {caracteristica}: {importancias[i]:.3f}")
    
    return modelo, scaler, label_encoder

def guardar_modelo(modelo, scaler, label_encoder):
    """Guarda el modelo y componentes"""
    try:
        # Guardar modelo
        with open('modelo_random_forest_vivino.pkl', 'wb') as f:
            pickle.dump(modelo, f)
        print("✅ Modelo guardado: modelo_random_forest_vivino.pkl")
        
        # Guardar scaler
        with open('scaler_vivino.pkl', 'wb') as f:
            pickle.dump(scaler, f)
        print("✅ Scaler guardado: scaler_vivino.pkl")
        
        # Guardar label encoder
        with open('label_encoder_vivino.pkl', 'wb') as f:
            pickle.dump(label_encoder, f)
        print("✅ Label encoder guardado: label_encoder_vivino.pkl")
        
    except Exception as e:
        print(f"❌ Error guardando modelo: {e}")

def main():
    """Función principal"""
    print("🍷 ENTRENAMIENTO DEL MODELO SOMMELIER")
    print("=" * 50)
    
    # Cargar datos
    df = cargar_datos()
    if df is None:
        return False
    
    # Limpiar datos
    resultado = limpiar_datos(df)
    if resultado is None:
        return False
    
    df_clean, caracteristicas = resultado
    
    # Entrenar modelo
    modelo, scaler, label_encoder = entrenar_modelo(df_clean, caracteristicas)
    
    # Guardar modelo
    guardar_modelo(modelo, scaler, label_encoder)
    
    print("\n✅ ENTRENAMIENTO COMPLETADO")
    print("🚀 Ahora puedes ejecutar: python app_sommelier.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("❌ Error en el entrenamiento")
        exit(1)
