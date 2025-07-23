#!/usr/bin/env python3
"""
Prueba del Modelo Entrenado con Datos de Vivino
Script para verificar que el modelo funciona correctamente
"""

import joblib
import numpy as np
import pandas as pd

def probar_modelo():
    """Prueba el modelo recién entrenado"""
    print("🧪 PROBANDO MODELO DE VINOS ENTRENADO")
    print("=" * 50)
    
    try:
        # Cargar modelo y componentes
        modelo = joblib.load('static/wine_model.pkl')
        scaler = joblib.load('static/wine_scaler.pkl')
        info_modelo = joblib.load('static/model_info.pkl')
        
        print("✅ Modelo cargado exitosamente")
        print(f"📊 Características: {len(info_modelo['caracteristicas'])}")
        print(f"🏷️ Clases: {info_modelo['clases_calidad']}")
        print(f"📅 Versión: {info_modelo['timestamp']}")
        
        # Crear datos de prueba
        print("\n🔬 Creando datos de prueba...")
        
        # Ejemplo 1: Vino económico con buen rating
        vino_economico = [
            15.50,  # precio_eur
            np.log1p(15.50),  # log_precio
            4.3,  # rating
            0.8,  # rating_normalizado (calculado)
            2021,  # año
            4,  # antiguedad
            150,  # num_reviews
            np.log1p(150),  # log_reviews
            2,  # region_especifica_encoded
            1,  # rango_precio_encoded
            2,  # rango_rating_encoded
            3,  # epoca_encoded
            5,  # bodega_simplificada_encoded
            15.50/4.3,  # precio_rating_ratio
            15.50/(4+1)  # precio_por_año
        ]
        
        # Ejemplo 2: Vino premium con rating alto
        vino_premium = [
            45.00,  # precio_eur
            np.log1p(45.00),  # log_precio
            4.5,  # rating
            1.0,  # rating_normalizado
            2020,  # año
            5,  # antiguedad
            500,  # num_reviews
            np.log1p(500),  # log_reviews
            1,  # region_especifica_encoded
            3,  # rango_precio_encoded
            3,  # rango_rating_encoded
            3,  # epoca_encoded
            2,  # bodega_simplificada_encoded
            45.00/4.5,  # precio_rating_ratio
            45.00/(5+1)  # precio_por_año
        ]
        
        # Ejemplo 3: Vino medio
        vino_medio = [
            25.00,  # precio_eur
            np.log1p(25.00),  # log_precio
            4.1,  # rating
            0.4,  # rating_normalizado
            2019,  # año
            6,  # antiguedad
            75,  # num_reviews
            np.log1p(75),  # log_reviews
            3,  # region_especifica_encoded
            2,  # rango_precio_encoded
            1,  # rango_rating_encoded
            2,  # epoca_encoded
            8,  # bodega_simplificada_encoded
            25.00/4.1,  # precio_rating_ratio
            25.00/(6+1)  # precio_por_año
        ]
        
        # Crear array de pruebas
        datos_prueba = np.array([vino_economico, vino_premium, vino_medio])
        
        # Escalar datos
        datos_escalados = scaler.transform(datos_prueba)
        
        # Realizar predicciones
        predicciones = modelo.predict(datos_escalados)
        probabilidades = modelo.predict_proba(datos_escalados)
        
        # Mostrar resultados
        print("\n🎯 RESULTADOS DE PREDICCIÓN:")
        print("-" * 50)
        
        nombres_vinos = ["Vino Económico (€15.50, Rating 4.3)", 
                        "Vino Premium (€45.00, Rating 4.5)", 
                        "Vino Medio (€25.00, Rating 4.1)"]
        
        for i, (nombre, pred, prob) in enumerate(zip(nombres_vinos, predicciones, probabilidades)):
            clase_predicha = info_modelo['clases_calidad'][pred]
            confianza = prob[pred] * 100
            
            print(f"\n{i+1}. {nombre}")
            print(f"   Predicción: {clase_predicha}")
            print(f"   Confianza: {confianza:.1f}%")
            
            # Mostrar probabilidades de todas las clases
            print("   Probabilidades por clase:")
            for j, clase in enumerate(info_modelo['clases_calidad']):
                print(f"     {clase}: {prob[j]*100:.1f}%")
        
        print(f"\n✅ MODELO FUNCIONANDO CORRECTAMENTE")
        print(f"📊 Predicciones generadas para {len(datos_prueba)} vinos de prueba")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando modelo: {e}")
        return False

if __name__ == "__main__":
    probar_modelo()
