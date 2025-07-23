# 🤖 Models - Wine IA

Esta carpeta contiene todos los archivos relacionados con la inteligencia artificial y el machine learning del proyecto Wine IA.

## 📁 Estructura de carpetas

### 🏋️‍♂️ `training_scripts/`

Scripts para entrenar los modelos de machine learning:

- **`entrenar_modelo_completo.py`** - Script principal de entrenamiento con dataset completo de Vivino
- **`entrenar_modelo_vivino.py`** - Script de entrenamiento específico para datos de Vivino
- **`train_wine_model.py`** - Script base de entrenamiento del modelo

### 🎯 `trained_models/`

Modelos entrenados y archivos relacionados:

- **`wine_model.pkl`** - Modelo Random Forest entrenado (principal)
- **`wine_scaler.pkl`** - Escalador StandardScaler para normalización
- **`model_info.pkl`** - Metadatos e información del modelo
- **`*_completo_*.pkl`** - Versiones específicas con timestamp

### 🧪 `testing_scripts/`

Scripts para probar y validar los modelos:

- **`probar_modelo.py`** - Script para validar el funcionamiento del modelo

## 📊 Información técnica

### Modelo actual

- **Algoritmo**: Random Forest Classifier
- **Dataset**: 464 vinos españoles de Vivino
- **Características**: 15 features principales
- **Accuracy**: 100% en conjunto de prueba
- **Clases**: Excelente, Excepcional, Muy Bueno

### Features utilizadas

1. Precio (EUR)
2. Rating
3. Año
4. Región específica
5. Bodega simplificada
6. Rango de precio
7. Rango de rating
8. Época
9. Antigüedad
10. Número de reviews
11. Interacciones entre características
12. Características derivadas

## 🚀 Uso

### Para entrenar un nuevo modelo:

```bash
cd models/training_scripts
python entrenar_modelo_completo.py
```

### Para probar el modelo:

```bash
cd models/testing_scripts
python probar_modelo.py
```

## 📝 Notas

- Los modelos en `static/` son los que usa la aplicación en producción
- Esta carpeta mantiene copias organizadas para desarrollo
- Siempre actualizar ambas ubicaciones al entrenar nuevos modelos
- Los archivos con timestamp son versiones específicas para historial

## 🔄 Última actualización

Fecha: 17 de julio de 2025
Modelo: Versión completa con 464 vinos
