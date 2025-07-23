# Guía de Configuración - Aplicación Web de Predicción de Dureza del Hormigón

## Resumen del Proyecto

Esta aplicación web utiliza Machine Learning para predecir la dureza del hormigón basándose en sus componentes químicos y edad. Utiliza un modelo entrenado guardado en formato pickle y una interfaz web desarrollada con Flask.

## Pasos Realizados para la Configuración

### 1. Verificación del Entorno Python

```bash
# Verificar versión de Python instalada
python --version
# Resultado: Python 3.12.10

# Verificar pip
pip --version
# Resultado: pip 25.0.1
```

### 2. Configuración del Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows PowerShell)
venv\Scripts\activate
```

### 3. Instalación de Dependencias

#### Librerías Core Necesarias:

```bash
# Instalación de paquetes principales
pip install flask pandas numpy scikit-learn xgboost
```

**Descripción de cada librería:**

- **Flask**: Framework web para Python que permite crear aplicaciones web
- **Pandas**: Manipulación y análisis de datos
- **Numpy**: Operaciones numéricas y arrays
- **Scikit-learn**: Librería de Machine Learning (para el scaler)
- **XGBoost**: Algoritmo de Machine Learning usado en el modelo entrenado

### 4. Estructura del Proyecto

```
hormigon_app/
├── app.py                 # Aplicación Flask principal
├── static/
│   ├── final_model.pkl    # Modelo entrenado guardado
│   └── scaler.pkl         # Scaler para normalización de datos
├── templates/
│   └── index.html         # Interfaz web HTML
└── venv/                  # Entorno virtual
```

### 5. Proceso de Carga de Modelos Pickle

#### En el archivo `app.py`:

```python
import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify

# Cargar el modelo y el scaler al iniciar la aplicación
model = pickle.load(open('static/final_model.pkl', 'rb'))
scaler = pickle.load(open('static/scaler.pkl', 'rb'))
```

**¿Qué son los archivos Pickle?**

- **final_model.pkl**: Contiene el modelo de Machine Learning entrenado (XGBoost)
- **scaler.pkl**: Contiene el StandardScaler para normalizar los datos de entrada

### 6. Implementación de la Lógica de Predicción

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # 1. Obtener datos del formulario web
            cement = float(request.form['cement'])
            slag = float(request.form['slag'])
            ash = float(request.form['ash'])
            water = float(request.form['water'])
            superplastic = float(request.form['superplastic'])
            coarseagg = float(request.form['coarseagg'])
            fineagg = float(request.form['fineagg'])
            age = float(request.form['age'])

            # 2. Crear DataFrame con los datos
            input_data = pd.DataFrame({
                'cement': [cement],
                'slag': [slag],
                'ash': [ash],
                'water': [water],
                'superplastic': [superplastic],
                'coarseagg': [coarseagg],
                'fineagg': [fineagg],
                'age': [age]
            })

            # 3. Normalizar los datos usando el scaler cargado
            scaled_data = scaler.transform(input_data)

            # 4. Hacer la predicción con el modelo cargado
            prediction = model.predict(scaled_data)

            # 5. Formatear el resultado
            prediction_rounded = round(prediction[0], 2)

            return render_template('index.html',
                                prediction_text=f'La dureza estimada del hormigón es: {prediction_rounded} MPa',
                                show_result=True)
        except Exception as e:
            return render_template('index.html',
                                prediction_text=f'Error: {str(e)}',
                                show_result=True)

    return render_template('index.html', show_result=False)
```

### 7. Integración con Flask

#### Configuración del servidor Flask:

```python
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)
```

### 8. Ejecución de la Aplicación

```bash
# Ejecutar la aplicación web
python app.py
```

**Resultado:**

- Servidor ejecutándose en: `http://127.0.0.1:5000`
- Modo debug activado para desarrollo

### 9. Flujo de Funcionamiento

1. **Inicio de la aplicación**: Flask carga los archivos pickle (modelo y scaler)
2. **Interfaz web**: El usuario introduce los parámetros del hormigón
3. **Procesamiento**: Los datos se normalizan con el scaler
4. **Predicción**: El modelo predice la dureza del hormigón
5. **Resultado**: Se muestra la predicción en la interfaz web

### 10. Parámetros de Entrada del Modelo

La aplicación requiere los siguientes parámetros:

- **Cement (Cemento)**: Cantidad en kg/m³
- **Slag (Escoria)**: Cantidad en kg/m³
- **Ash (Ceniza)**: Cantidad en kg/m³
- **Water (Agua)**: Cantidad en kg/m³
- **Superplastic (Superplastificante)**: Cantidad en kg/m³
- **Coarseagg (Agregado grueso)**: Cantidad en kg/m³
- **Fineagg (Agregado fino)**: Cantidad en kg/m³
- **Age (Edad)**: Días de curado

### 11. Advertencias Encontradas

Durante la ejecución se presentaron advertencias sobre versiones:

- **XGBoost**: Modelo guardado con versión anterior
- **Scikit-learn**: Scaler guardado con versión 1.6.1, usando 1.7.0

**Nota**: Estas advertencias no afectan el funcionamiento de la aplicación.

### 12. Comandos de Mantenimiento

```bash
# Ver paquetes instalados
pip list

# Crear archivo de requerimientos
pip freeze > requirements.txt

# Instalar desde requirements.txt
pip install -r requirements.txt

# Desactivar entorno virtual
deactivate
```

## Conclusión

La aplicación web está completamente funcional y permite:

- Cargar modelos de Machine Learning desde archivos pickle
- Procesar datos de entrada del usuario
- Realizar predicciones en tiempo real
- Mostrar resultados a través de una interfaz web amigable

La integración entre los archivos pickle y Flask permite una aplicación web eficiente que mantiene el modelo cargado en memoria para respuestas rápidas.
