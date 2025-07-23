#!/usr/bin/env python3
"""
Entrenamiento de Modelo de ML con Datos Completos de Vivino
Script para entrenar un modelo mejorado con todos los datos de scraping
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ModeloVinoCompleto:
    """Modelo completo de clasificación de vinos con datos de Vivino"""
    
    def __init__(self):
        self.modelo = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.caracteristicas = []
        self.clases_calidad = []
        
    def cargar_datos_completos(self, archivo_csv):
        """Carga y procesa los datos completos del scraping"""
        print("📊 Cargando datos completos de Vivino...")
        
        try:
            # Cargar datos
            df = pd.read_csv(archivo_csv, encoding='utf-8')
            print(f"✅ Datos cargados: {len(df)} registros")
            
            # Mostrar información básica
            print(f"📊 Columnas disponibles: {list(df.columns)}")
            print(f"📊 Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            return df
            
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return None
    
    def limpiar_datos(self, df):
        """Limpia y prepara los datos para el entrenamiento"""
        print("🧹 Limpiando y preparando datos...")
        
        # Eliminar duplicados por URL para tener vinos únicos
        df_original_size = len(df)
        df = df.drop_duplicates(subset=['url'], keep='first')
        duplicados_eliminados = df_original_size - len(df)
        print(f"🗑️ Duplicados eliminados: {duplicados_eliminados}")
        print(f"✅ Vinos únicos: {len(df)}")
        
        # Limpiar valores nulos en columnas críticas
        columnas_criticas = ['precio_eur', 'rating', 'año', 'region', 'bodega']
        for col in columnas_criticas:
            if col in df.columns:
                antes = len(df)
                df = df.dropna(subset=[col])
                despues = len(df)
                if antes != despues:
                    print(f"   {col}: eliminados {antes-despues} registros con valores nulos")
        
        # Normalizar región (algunos están como 'España' genérico)
        if 'region' in df.columns:
            # Mapear regiones genéricas a específicas basándose en bodega
            df['region'] = df['region'].fillna('España')
            
            # Crear mapeo de regiones más específico
            mapeo_regiones = {
                'España': 'Otras Regiones',
                'Campo de Borja': 'Aragón - Campo de Borja',
                'Calatayud': 'Aragón - Calatayud',
                'Madrid': 'Madrid',
                'Terra Alta': 'Cataluña - Terra Alta',
                'Castilla y León': 'Castilla y León',
                'Aragón': 'Aragón - General',
                'Navarra': 'Navarra',
                'Empordà': 'Cataluña - Empordà',
                'Valdejalón': 'Aragón - Valdejalón',
                'Cataluña': 'Cataluña - General',
                'Cariñena': 'Aragón - Cariñena',
                'Somontano': 'Aragón - Somontano',
                'Penedès': 'Cataluña - Penedès',
                'Costers del Segre': 'Cataluña - Costers del Segre'
            }
            
            df['region_especifica'] = df['region'].map(mapeo_regiones).fillna(df['region'])
        
        # Normalizar categorías de calidad
        if 'categoria_calidad' in df.columns:
            df['categoria_calidad'] = df['categoria_calidad'].fillna('Standard')
            
            # Mapear categorías similares
            mapeo_calidad = {
                'Great Value': 'Excellent Value',
                'Good Value': 'Good Value',
                'Amazing Value': 'Excellent Value',
                'Best Value': 'Excellent Value',
                'Excellent Value': 'Excellent Value',
                'Outstanding Value': 'Excellent Value',
                'Cosecha más antigua': 'Vintage',
                'Premium': 'Premium',
                'Limited Edition': 'Premium',
                'Organic': 'Specialty',
                'Top Rated': 'Premium',
                'Critics Choice': 'Premium'
            }
            
            df['categoria_calidad_normalizada'] = df['categoria_calidad'].map(mapeo_calidad).fillna('Standard')
        
        # Crear características derivadas
        if 'año' in df.columns:
            df['año'] = df['año'].astype(int)
            df['antiguedad'] = 2025 - df['año']
            df['epoca'] = pd.cut(df['año'], 
                               bins=[1990, 2000, 2010, 2015, 2020, 2025],
                               labels=['Clásicos', 'Millennium', 'Década 2010', 'Modernos', 'Recientes'])
        
        # Crear rangos de precio
        if 'precio_eur' in df.columns:
            df['rango_precio'] = pd.cut(df['precio_eur'],
                                      bins=[0, 15, 25, 40, 60, 100],
                                      labels=['Económico', 'Medio', 'Premium', 'Lujo', 'Ultra-Premium'])
        
        # Crear rangos de rating
        if 'rating' in df.columns:
            df['rango_rating'] = pd.cut(df['rating'],
                                      bins=[0, 4.0, 4.2, 4.4, 5.0],
                                      labels=['Bueno', 'Muy Bueno', 'Excelente', 'Excepcional'])
        
        # Extraer características de bodega
        if 'bodega' in df.columns:
            # Simplificar nombres de bodega (primeras dos palabras)
            df['bodega_simplificada'] = df['bodega'].str.split().str[:2].str.join(' ')
            df['bodega_simplificada'] = df['bodega_simplificada'].str.replace(r'[^\w\s]', '', regex=True)
        
        print(f"✅ Datos limpios: {len(df)} vinos únicos")
        return df
    
    def ingenieria_caracteristicas(self, df):
        """Aplica ingeniería de características avanzada"""
        print("🔧 Aplicando ingeniería de características...")
        
        # Características numéricas
        caracteristicas_numericas = []
        
        if 'precio_eur' in df.columns:
            caracteristicas_numericas.append('precio_eur')
            # Log del precio para normalizar distribución
            df['log_precio'] = np.log1p(df['precio_eur'])
            caracteristicas_numericas.append('log_precio')
        
        if 'rating' in df.columns:
            caracteristicas_numericas.append('rating')
            # Rating normalizado
            df['rating_normalizado'] = (df['rating'] - df['rating'].min()) / (df['rating'].max() - df['rating'].min())
            caracteristicas_numericas.append('rating_normalizado')
        
        if 'año' in df.columns:
            caracteristicas_numericas.extend(['año', 'antiguedad'])
        
        if 'num_reviews' in df.columns:
            df['num_reviews'] = df['num_reviews'].fillna(0)
            caracteristicas_numericas.append('num_reviews')
            # Log de reviews
            df['log_reviews'] = np.log1p(df['num_reviews'])
            caracteristicas_numericas.append('log_reviews')
        
        # Características categóricas
        caracteristicas_categoricas = []
        
        for col in ['region_especifica', 'rango_precio', 'rango_rating', 'epoca', 'bodega_simplificada']:
            if col in df.columns:
                caracteristicas_categoricas.append(col)
        
        # Codificar características categóricas
        for col in caracteristicas_categoricas:
            le = LabelEncoder()
            df[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))
            self.label_encoders[col] = le
            caracteristicas_numericas.append(f'{col}_encoded')
        
        # Interacciones entre características
        if 'precio_eur' in df.columns and 'rating' in df.columns:
            df['precio_rating_ratio'] = df['precio_eur'] / df['rating']
            caracteristicas_numericas.append('precio_rating_ratio')
        
        if 'precio_eur' in df.columns and 'antiguedad' in df.columns:
            df['precio_por_año'] = df['precio_eur'] / (df['antiguedad'] + 1)
            caracteristicas_numericas.append('precio_por_año')
        
        self.caracteristicas = caracteristicas_numericas
        print(f"✅ Características creadas: {len(self.caracteristicas)}")
        print(f"📊 Lista de características: {self.caracteristicas}")
        
        return df
    
    def definir_variable_objetivo(self, df):
        """Define la variable objetivo para la clasificación"""
        print("🎯 Definiendo variable objetivo...")
        
        # Crear una variable objetivo basada en múltiples factores
        # Combinar rating, precio y categoría de calidad
        
        # Base: categoría de rating
        df['calidad_objetivo'] = df['rango_rating'].astype(str)
        
        # Ajustar por categoría de calidad si existe
        if 'categoria_calidad_normalizada' in df.columns:
            # Promover vinos con categorías especiales
            mask_premium = df['categoria_calidad_normalizada'].isin(['Premium', 'Excellent Value'])
            df.loc[mask_premium & (df['rango_rating'] == 'Muy Bueno'), 'calidad_objetivo'] = 'Excelente'
            
            mask_specialty = df['categoria_calidad_normalizada'].isin(['Vintage', 'Specialty'])
            df.loc[mask_specialty & (df['rango_rating'].isin(['Muy Bueno', 'Excelente'])), 'calidad_objetivo'] = 'Excepcional'
        
        # Codificar variable objetivo
        le_objetivo = LabelEncoder()
        df['calidad_numerica'] = le_objetivo.fit_transform(df['calidad_objetivo'])
        self.label_encoders['objetivo'] = le_objetivo
        self.clases_calidad = le_objetivo.classes_
        
        print(f"✅ Clases de calidad definidas: {self.clases_calidad}")
        print(f"📊 Distribución de clases:")
        distribucion = df['calidad_objetivo'].value_counts()
        for clase, count in distribucion.items():
            porcentaje = count / len(df) * 100
            print(f"   {clase}: {count} vinos ({porcentaje:.1f}%)")
        
        return df
    
    def entrenar_modelo(self, df):
        """Entrena el modelo de clasificación"""
        print("🚀 Entrenando modelo de clasificación...")
        
        # Preparar datos
        X = df[self.caracteristicas].fillna(0)
        y = df['calidad_numerica']
        
        print(f"📊 Características: {X.shape[1]}")
        print(f"📊 Muestras: {X.shape[0]}")
        
        # Escalar características numéricas
        X_scaled = self.scaler.fit_transform(X)
        
        # División de datos
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"📊 Datos de entrenamiento: {X_train.shape[0]}")
        print(f"📊 Datos de prueba: {X_test.shape[0]}")
        
        # Búsqueda de hiperparámetros
        print("🔍 Optimizando hiperparámetros...")
        
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2', None]
        }
        
        rf_base = RandomForestClassifier(random_state=42, n_jobs=-1)
        
        # Usar validación cruzada para encontrar mejores parámetros
        grid_search = GridSearchCV(
            rf_base, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        print(f"✅ Mejores parámetros: {grid_search.best_params_}")
        print(f"✅ Mejor score CV: {grid_search.best_score_:.4f}")
        
        # Entrenar modelo final
        self.modelo = grid_search.best_estimator_
        
        # Evaluar en datos de prueba
        y_pred = self.modelo.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✅ Accuracy en prueba: {accuracy:.4f}")
        print(f"✅ Accuracy en prueba: {accuracy*100:.2f}%")
        
        # Reporte detallado
        print("\n📊 REPORTE DE CLASIFICACIÓN:")
        print(classification_report(y_test, y_pred, target_names=self.clases_calidad))
        
        # Importancia de características
        print("\n🔍 IMPORTANCIA DE CARACTERÍSTICAS:")
        importancias = self.modelo.feature_importances_
        for i, importancia in enumerate(importancias):
            if importancia > 0.05:  # Solo mostrar características importantes
                print(f"   {self.caracteristicas[i]}: {importancia:.4f}")
        
        return accuracy
    
    def guardar_modelo(self):
        """Guarda el modelo entrenado y componentes"""
        print("💾 Guardando modelo...")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Crear carpeta static si no existe
            if not os.path.exists('static'):
                os.makedirs('static')
            
            # Guardar modelo
            modelo_path = f'static/wine_model_completo_{timestamp}.pkl'
            joblib.dump(self.modelo, modelo_path)
            
            # Guardar scaler
            scaler_path = f'static/wine_scaler_completo_{timestamp}.pkl'
            joblib.dump(self.scaler, scaler_path)
            
            # Guardar información del modelo
            info_modelo = {
                'caracteristicas': self.caracteristicas,
                'label_encoders': self.label_encoders,
                'clases_calidad': self.clases_calidad.tolist(),
                'timestamp': timestamp,
                'version': 'completa'
            }
            
            info_path = f'static/model_info_completo_{timestamp}.pkl'
            joblib.dump(info_modelo, info_path)
            
            # Actualizar archivos principales (para compatibilidad)
            joblib.dump(self.modelo, 'static/wine_model.pkl')
            joblib.dump(self.scaler, 'static/wine_scaler.pkl')
            joblib.dump(info_modelo, 'static/model_info.pkl')
            
            print(f"✅ Modelo guardado:")
            print(f"   - Modelo: {modelo_path}")
            print(f"   - Scaler: {scaler_path}")
            print(f"   - Info: {info_path}")
            print(f"✅ Archivos principales actualizados para compatibilidad")
            
        except Exception as e:
            print(f"❌ Error guardando modelo: {e}")
    
    def entrenar_modelo_completo(self, archivo_csv):
        """Proceso completo de entrenamiento"""
        print("🍷 ENTRENAMIENTO COMPLETO DE MODELO DE VINOS - VIVINO")
        print("=" * 60)
        
        # Cargar datos
        df = self.cargar_datos_completos(archivo_csv)
        if df is None:
            return False
        
        # Limpiar datos
        df = self.limpiar_datos(df)
        
        # Ingeniería de características
        df = self.ingenieria_caracteristicas(df)
        
        # Definir variable objetivo
        df = self.definir_variable_objetivo(df)
        
        # Entrenar modelo
        accuracy = self.entrenar_modelo(df)
        
        # Guardar modelo
        self.guardar_modelo()
        
        print(f"\n✅ ENTRENAMIENTO COMPLETADO")
        print(f"🎯 Accuracy final: {accuracy*100:.2f}%")
        print(f"🍷 Vinos utilizados: {len(df)}")
        print(f"📊 Características: {len(self.caracteristicas)}")
        print(f"🏷️ Clases de calidad: {len(self.clases_calidad)}")
        
        return True


def main():
    """Función principal para entrenar el modelo"""
    # Archivo con datos completos
    archivo_datos = "datos_scraping/resumen_scraping_completo_20250716_130237.csv"
    
    # Verificar que existe el archivo
    if not os.path.exists(archivo_datos):
        print(f"❌ No se encuentra el archivo: {archivo_datos}")
        return False
    
    # Crear y entrenar modelo
    modelo_completo = ModeloVinoCompleto()
    exito = modelo_completo.entrenar_modelo_completo(archivo_datos)
    
    if exito:
        print("\n🎉 MODELO ENTRENADO EXITOSAMENTE")
        print("📁 Archivos del modelo guardados en carpeta 'static'")
        print("🚀 El modelo está listo para ser usado en la aplicación")
    else:
        print("\n❌ ERROR EN EL ENTRENAMIENTO")
    
    return exito


if __name__ == "__main__":
    main()
