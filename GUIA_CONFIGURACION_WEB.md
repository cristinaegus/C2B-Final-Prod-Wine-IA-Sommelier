# Guía de Configuración - Aplicación Web de Predicción de Calidad de Vino 🍷

## Resumen del Proyecto

Esta aplicación web utiliza Machine Learning para predecir la calidad del vino basándose en sus características químicas. Utiliza un modelo entrenado con el dataset Wine Quality y una interfaz web desarrollada con Flask.

## Estructura del Proyecto

```
Wine_Analysis_V2/
├── app.py                          # Aplicación Flask principal
├── train_model.py                  # Script para entrenar el modelo
├── wine_model.pkl                  # Modelo entrenado (generado)
├── winequality-red.csv            # Dataset de vinos
├── requirements.txt               # Dependencias del proyecto
├── templates/                     # Plantillas HTML
│   ├── index.html                # Formulario principal
│   ├── result.html               # Página de resultados
│   └── about.html                # Información del modelo
├── Wine_multiclass_classification__97_5_accuracy.ipynb  # Notebook original
└── GUIA_CONFIGURACION_WEB.md     # Esta guía
```

## Pasos para Configurar la Aplicación Web

### 1. Verificación del Entorno Python

```powershell
# Verificar versión de Python instalada
python --version
# Resultado esperado: Python 3.12.10 o superior

# Verificar pip
pip --version
```

### 2. Activar el Entorno Virtual

```powershell
# Navegar al directorio del proyecto
cd "c:\Users\Dell\PyhtonIA\Wine_Analysis_V2"

# Activar entorno virtual (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Verificar que el entorno está activado (debería mostrar (.venv) al inicio)
```

### 3. Instalar Dependencias

```powershell
# Instalar todas las dependencias desde requirements.txt
pip install -r requirements.txt

# Verificar instalaciones clave
pip show flask pandas scikit-learn xgboost
```

#### Librerías Principales:

- **Flask**: Framework web para Python
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Operaciones numéricas
- **Scikit-learn**: Machine Learning y preprocesamiento
- **XGBoost**: Algoritmo de Machine Learning avanzado
- **Imbalanced-learn**: Balanceado de clases
- **Matplotlib/Seaborn**: Visualización de datos

### 4. Entrenar el Modelo (Primera vez)

```powershell
# Ejecutar el script de entrenamiento
python train_model.py
```

**Salida esperada:**

```
🍷 === ENTRENAMIENTO DEL MODELO DE CALIDAD DE VINO ===

🍷 Cargando datos del vino...
✅ Datos cargados: 1599 muestras, 12 características
📊 Distribución original de calidad:
3      10
4      53
5     681
6     638
7     199
8      18

🔧 Preprocesando datos...
⚖️ Balanceando clases con SMOTEENN...
📈 Datos después del balanceado: 4068 muestras
...
🎯 Precisión del modelo: 0.9750 (97.50%)
✅ Modelo guardado en 'wine_model.pkl'
🎉 ¡Entrenamiento completado exitosamente!
```

### 5. Ejecutar la Aplicación Web

```powershell
# Ejecutar la aplicación Flask
python app.py
```

**Salida esperada:**

```
✅ Modelo cargado exitosamente
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[tu-ip]:5000
```

### 6. Acceder a la Aplicación

Abre tu navegador web y ve a:

- **Aplicación principal**: http://localhost:5000
- **Información del modelo**: http://localhost:5000/about

## Características de la Aplicación Web

### 🏠 Página Principal (`/`)

- **Formulario interactivo** para introducir las 11 características del vino
- **Validación en tiempo real** de los valores introducidos
- **Datos de ejemplo** precargados para pruebas rápidas
- **Interfaz responsiva** que funciona en móviles y escritorio

### 📊 Página de Resultados (`/predict`)

- **Predicción de calidad** en escala 3-8
- **Gráfico de probabilidades** para todas las clases
- **Interpretación del resultado** con recomendaciones
- **Listado detallado** de las características analizadas

### ℹ️ Página de Información (`/about`)

- **Detalles técnicos** del modelo de Machine Learning
- **Estadísticas de rendimiento** (97.5% de precisión)
- **Descripción de características** químicas analizadas
- **Limitaciones y recomendaciones** de uso

### 🔌 API REST (`/api/predict`)

- **Endpoint JSON** para integraciones externas
- **Formato de entrada estándar**
- **Respuestas estructuradas** con probabilidades

## Ejemplo de Uso de la API

```python
import requests
import json

# Datos de ejemplo
wine_data = {
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.7,
    "citric_acid": 0.0,
    "residual_sugar": 1.9,
    "chlorides": 0.076,
    "free_sulfur_dioxide": 11,
    "total_sulfur_dioxide": 34,
    "density": 0.9978,
    "pH": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4
}

# Realizar predicción
response = requests.post(
    'http://localhost:5000/api/predict',
    json=wine_data,
    headers={'Content-Type': 'application/json'}
)

result = response.json()
print(f"Calidad predicha: {result['predicted_quality']}")
print(f"Probabilidades: {result['probabilities']}")
```

## Características del Modelo

### 📈 Rendimiento

- **Precisión**: 97.5% en el conjunto de prueba
- **Algoritmo**: Random Forest Classifier
- **Muestras de entrenamiento**: 4,068 (después del balanceado)
- **Características**: 11 propiedades químicas

### 🧪 Características Analizadas

1. **Acidez Fija** (g/L) - Ácidos no volátiles
2. **Acidez Volátil** (g/L) - Cantidad de ácido acético
3. **Ácido Cítrico** (g/L) - Conservante natural
4. **Azúcar Residual** (g/L) - Azúcar después de fermentación
5. **Cloruros** (g/L) - Cantidad de sal
6. **SO₂ Libre** (mg/L) - Dióxido de azufre libre
7. **SO₂ Total** (mg/L) - Dióxido de azufre total
8. **Densidad** (g/cm³) - Densidad relativa al agua
9. **pH** - Nivel de acidez/alcalinidad
10. **Sulfatos** (g/L) - Aditivos antimicrobianos
11. **Alcohol** (% vol) - Porcentaje de alcohol

### 🎯 Clases de Calidad

- **3-4**: Calidad baja a regular
- **5-6**: Calidad buena a muy buena
- **7-8**: Calidad excelente a excepcional

## Solución de Problemas Comunes

### ❌ Error: "No se ha podido resolver la importación flask"

```powershell
# Verificar que el entorno virtual está activado
.venv\Scripts\Activate.ps1

# Reinstalar Flask
pip install flask
```

### ❌ Error: "No se encontró archivo winequality-red.csv"

```powershell
# Verificar que el archivo está en el directorio correcto
ls winequality-red.csv

# Si no existe, verificar que estás en el directorio correcto
pwd
```

### ❌ Error: "Port 5000 is already in use"

```powershell
# Cambiar puerto en app.py (línea final)
app.run(debug=True, host='0.0.0.0', port=5001)
```

### ❌ Problema: Kernel no aparece en el notebook

```powershell
# Registrar kernel del entorno virtual
python -m ipykernel install --user --name=wine-analysis --display-name="Wine Analysis (.venv)"

# Reiniciar VS Code después de registrar el kernel
```

## Archivos Importantes

### 📄 `app.py`

Aplicación Flask principal con todas las rutas y lógica de predicción.

### 📄 `train_model.py`

Script para entrenar y guardar el modelo. Incluye todo el pipeline de preprocesamiento.

### 📄 `wine_model.pkl`

Modelo entrenado serializado que incluye:

- Modelo Random Forest entrenado
- Scaler para normalización
- Label encoder para clases
- Power transformer para características sesgadas

### 📁 `templates/`

Plantillas HTML con Bootstrap para la interfaz web.

## Comandos Útiles

```powershell
# Activar entorno y ejecutar aplicación (comando completo)
.venv\Scripts\Activate.ps1; python app.py

# Reinstalar dependencias
pip install -r requirements.txt --upgrade

# Verificar estado del modelo
python -c "import pickle; data = pickle.load(open('wine_model.pkl', 'rb')); print(f'Precisión: {data[\"accuracy\"]:.4f}')"

# Generar nuevo archivo requirements.txt
pip freeze > requirements_new.txt
```

## Próximos Pasos

1. **🚀 Despliegue**: Considera usar Heroku, Railway o Vercel para desplegar la aplicación
2. **📱 Mejoras UI**: Añadir más gráficos interactivos con Chart.js
3. **🔐 Seguridad**: Implementar autenticación si es necesario
4. **📊 Logging**: Añadir registro de predicciones para análisis
5. **🧪 Más Modelos**: Experimentar con otros algoritmos como XGBoost

## Contacto y Soporte

- **Repositorio**: Basado en Wine Quality Dataset (UCI ML Repository)
- **Tecnologías**: Python 3.12, Flask, Scikit-learn, Bootstrap 5
- **Última actualización**: Enero 2025

---

¡La aplicación web está lista para usar! 🎉🍷
