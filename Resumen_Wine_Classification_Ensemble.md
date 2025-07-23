# Resumen: Clasificación de Calidad de Vino con Modelos Ensemble

## 📊 Información General del Proyecto

**Dataset:** Wine Quality (Vino Tinto)  
**Objetivo:** Clasificación multiclase de calidad de vino (escala 3-8)  
**Técnicas:** Comparación de modelos Bagging vs Boosting  
**Accuracy máximo alcanzado:** 97.5% (XGBoost)

---

## 🔧 1. Preparación del Entorno

### Configuración inicial:

- ✅ Creación de entorno virtual Python 3.12.10
- ✅ Instalación de librerías necesarias:
  - `pandas`, `numpy`: Manipulación de datos
  - `scikit-learn`: Machine Learning
  - `matplotlib`, `seaborn`: Visualización
  - `xgboost`: Gradient Boosting avanzado
  - `imbalanced-learn`: Balanceo de clases
  - `kagglehub`: Descarga de datasets

### Importación de datos:

- Archivo fuente: `winequality-red.csv`
- Dimensiones originales: 1,599 filas × 12 columnas
- Variables: 11 características fisicoquímicas + 1 variable objetivo (quality)

---

## 📈 2. Análisis Exploratorio de Datos (EDA)

### 2.1 Inspección inicial:

- **Filas duplicadas:** 240 encontradas y eliminadas
- **Valores nulos:** 0 (dataset limpio)
- **Distribución de calidad:** Clases desbalanceadas (principalmente 5 y 6)

### 2.2 Análisis de correlaciones:

- **Correlación positiva con calidad:** alcohol (0.48), sulphates (0.25)
- **Correlación negativa con calidad:** volatile acidity (-0.39)
- **Sin multicolinealidad:** No hay características altamente correlacionadas entre sí

### 2.3 Distribución de clases originales:

- Calidad 3: 10 muestras (0.6%)
- Calidad 4: 53 muestras (3.3%)
- Calidad 5: 681 muestras (42.6%) ⚠️
- Calidad 6: 638 muestras (39.9%) ⚠️
- Calidad 7: 199 muestras (12.4%)
- Calidad 8: 18 muestras (1.1%)

---

## ⚖️ 3. Preprocesamiento de Datos

### 3.1 Balanceo de clases:

- **Técnica:** SMOTEENN (combinación de SMOTE + Edited Nearest Neighbours)
- **Resultado:** ~470 muestras por clase (distribución balanceada)
- **Dataset final:** 2,828 muestras

### 3.2 Transformación de etiquetas:

- **Problema:** XGBoost requiere etiquetas 0-5, no 3-8
- **Solución:** LabelEncoder para mapear calidades:
  - Calidad 3 → 0, Calidad 4 → 1, ..., Calidad 8 → 5

### 3.3 División de datos:

- **Training:** 80% (2,262 muestras)
- **Testing:** 20% (566 muestras)
- **Estrategia:** train_test_split con random_state=42

### 3.4 Tratamiento de asimetría:

- **Columnas asimétricas identificadas:** 6 variables
  - chlorides, residual sugar, total sulfur dioxide
  - sulphates, free sulfur dioxide, volatile acidity
- **Transformación:** PowerTransformer (Yeo-Johnson)

### 3.5 Escalado de características:

- **Técnica:** MinMaxScaler (0-1)
- **Aplicación:** Todas las características después de transformaciones

---

## 🤖 4. Modelado y Evaluación

### 4.1 Modelos Base Individuales:

| Modelo                    | Accuracy | Observaciones             |
| ------------------------- | -------- | ------------------------- |
| Logistic Regression       | ~85%     | Modelo lineal base        |
| K-Nearest Neighbors       | 97.2%    | Excelente con k=1         |
| Support Vector Classifier | 97.2%    | Kernel RBF, C=100         |
| Decision Tree             | ~93%     | Susceptible a overfitting |

### 4.2 Modelos Ensemble Originales:

| Modelo            | Accuracy  | Tipo            |
| ----------------- | --------- | --------------- |
| Random Forest     | 95.9%     | Bagging         |
| Gradient Boosting | 97.2%     | Boosting        |
| **XGBoost**       | **97.5%** | **Boosting** 🏆 |

---

## 🆚 5. Comparación Detallada: Bagging vs Boosting

### 5.1 Modelos de Bagging:

| Modelo                   | Accuracy | Descripción                                      |
| ------------------------ | -------- | ------------------------------------------------ |
| Bagging + Decision Trees | ~95%     | Bootstrap + árboles paralelos                    |
| Random Forest            | ~96%     | Bagging + selección aleatoria de características |
| Extra Trees              | ~95%     | Más aleatorio que Random Forest                  |

**Promedio Bagging:** ~95.3%

### 5.2 Modelos de Boosting:

| Modelo            | Accuracy | Descripción                  |
| ----------------- | -------- | ---------------------------- |
| AdaBoost          | ~92%     | Ajuste secuencial de pesos   |
| Gradient Boosting | ~97%     | Minimización de gradiente    |
| XGBoost           | ~97.5%   | Gradient Boosting optimizado |

**Promedio Boosting:** ~95.5%

### 5.3 Resultado de la Comparación:

🏆 **GANADOR: Modelos de Boosting** (por margen mínimo)

---

## 📊 6. Visualizaciones Creadas

### 6.1 Análisis exploratorio:

- ✅ Heatmap de correlaciones
- ✅ Distribución de clases (antes/después del balanceo)
- ✅ Histogramas y boxplots por característica
- ✅ Gráficos de barras: características vs calidad

### 6.2 Evaluación de modelos:

- ✅ Comparación de accuracy por modelo
- ✅ Promedio Bagging vs Boosting
- ✅ Matrices de confusión (Random Forest vs XGBoost)
- ✅ Reporte de clasificación detallado

---

## 🎯 7. Conclusiones Principales

### 7.1 Rendimiento de modelos:

1. **Mejor modelo individual:** XGBoost (97.5%)
2. **Mejores modelos base:** KNN y SVC (97.2%)
3. **Modelo más consistente:** Random Forest (96%+)

### 7.2 Bagging vs Boosting:

- **Boosting** ligeramente superior en promedio
- **Bagging** más estable y menos propenso a overfitting
- **Diferencia mínima:** ~0.2% entre enfoques

### 7.3 Factores clave del éxito:

- ✅ Balanceo efectivo de clases con SMOTEENN
- ✅ Transformación adecuada de características asimétricas
- ✅ Escalado apropiado de variables
- ✅ Transformación correcta de etiquetas para XGBoost

### 7.4 Características más importantes:

- **Alcohol:** Correlación más fuerte con calidad
- **Sulphates:** Segundo predictor más importante
- **Volatile acidity:** Correlación negativa significativa

---

## 🔧 8. Aspectos Técnicos Destacados

### 8.1 Desafíos resueltos:

- **Clases desbalanceadas:** SMOTEENN balanceó efectivamente
- **Etiquetas incompatibles:** LabelEncoder para XGBoost
- **Características asimétricas:** PowerTransformer normalizó distribuciones
- **Escalas diferentes:** MinMaxScaler estandarizó rangos

### 8.2 Mejores prácticas aplicadas:

- Validación cruzada implícita en ensemble methods
- Uso de random_state para reproducibilidad
- División estratificada de datos
- Evaluación con múltiples métricas

### 8.3 Configuraciones óptimas:

- **Random Forest:** 100 estimadores, características aleatorias
- **XGBoost:** learning_rate=0.1, max_depth=3, 100 estimadores
- **Gradient Boosting:** learning_rate=0.1, max_depth=3

---

## 📁 9. Archivos del Proyecto

```
ML Modelos Ensemble/
├── Wine_multiclass_classification__97_5_accuracy.ipynb
├── winequality-red.csv
├── churn.csv
├── .gitignore
├── .venv/
└── Resumen_Wine_Classification_Ensemble.md
```

---

## 🚀 10. Próximos Pasos Sugeridos

### 10.1 Mejoras potenciales:

- [ ] Hyperparameter tuning con GridSearchCV
- [ ] Ensemble voting (combinación de mejores modelos)
- [ ] Feature engineering adicional
- [ ] Validación cruzada estratificada explícita

### 10.2 Experimentación adicional:

- [ ] Otros algoritmos de balanceo (ADASYN, BorderlineSMOTE)
- [ ] Técnicas de selección de características
- [ ] Modelos de deep learning
- [ ] Análisis de importancia de características

### 10.3 Deployment:

- [ ] Creación de API para predicciones
- [ ] Containerización con Docker
- [ ] Interfaz web con Streamlit/Flask
- [ ] Monitoreo de modelo en producción

---

**Fecha de creación:** 8 de julio de 2025  
**Autor:** Análisis de clasificación de vino con modelos ensemble  
**Accuracy máximo alcanzado:** 97.5% con XGBoost  
**Técnicas clave:** Bagging, Boosting, SMOTEENN, PowerTransformer


About CSV

About this file
Context

This datasets is related to red variants of the Portuguese "Vinho Verde" wine. For more details, consult the reference [Cortez et al., 2009]. Due to privacy and logistic issues, only physicochemical (inputs) and sensory (the output) variables are available (e.g. there is no data about grape types, wine brand, wine selling price, etc.).

The datasets can be viewed as classification or regression tasks. The classes are ordered and not balanced (e.g. there are much more normal wines than excellent or poor ones).

This dataset is also available from the UCI machine learning repository, https://archive.ics.uci.edu/ml/datasets/wine+quality , I just shared it to kaggle for convenience. (If I am mistaken and the public license type disallowed me from doing so, I will take this down if requested.)

Content

For more information, read [Cortez et al., 2009].
Input variables (based on physicochemical tests):
1 - fixed acidity
2 - volatile acidity
3 - citric acid
4 - residual sugar
5 - chlorides
6 - free sulfur dioxide
7 - total sulfur dioxide
8 - density
9 - pH
10 - sulphates
11 - alcohol
Output variable (based on sensory data):
12 - quality (score between 0 and 10)

Tips

What might be an interesting thing to do, is aside from using regression modelling, is to set an arbitrary cutoff for your dependent variable (wine quality) at e.g. 7 or higher getting classified as 'good/1' and the remainder as 'not good/0'. This allows you to practice with hyper parameter tuning on e.g. decision tree algorithms looking at the ROC curve and the AUC value. Without doing any kind of feature engineering or overfitting you should be able to get an AUC of .88 (without even using random forest algorithm)

KNIME is a great tool (GUI) that can be used for this.
1 - File Reader (for csv) to linear correlation node and to interactive histogram for basic EDA.
2- File Reader to 'Rule Engine Node' to turn the 10 point scale to dichtome variable (good wine and rest), the code to put in the rule engine is something like this:

$quality$ > 6.5 => "good"
TRUE => "bad"
3- Rule Engine Node output to input of Column Filter node to filter out your original 10point feature (this prevent leaking)
4- Column Filter Node output to input of Partitioning Node (your standard train/tes split, e.g. 75%/25%, choose 'random' or 'stratified')
5- Partitioning Node train data split output to input of Train data split to input Decision Tree Learner node and
6- Partitioning Node test data split output to input Decision Tree predictor Node
7- Decision Tree learner Node output to input Decision Tree Node input
8- Decision Tree output to input ROC Node.. (here you can evaluate your model base on AUC value)
Inspiration

Use machine learning to determine which physiochemical properties make a wine 'good'!

Acknowledgements

This dataset is also available from the UCI machine learning repository, https://archive.ics.uci.edu/ml/datasets/wine+quality , I just shared it to kaggle for convenience. (I am mistaken and the public license type disallowed me from doing so, I will take this down at first request. I am not the owner of this dataset.

Please include this citation if you plan to use this database:
P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis. Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.

Relevant publication