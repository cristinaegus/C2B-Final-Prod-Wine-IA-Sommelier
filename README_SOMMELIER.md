# 🍷 Sommelier Inteligente - Sistema de Recomendación de Vinos

## 🎯 Descripción

El **Sommelier Inteligente** es un sistema de recomendación personalizada de vinos españoles que utiliza Machine Learning y datos reales extraídos de Vivino. A diferencia del clasificador de calidad tradicional, este sistema se enfoca en encontrar el vino perfecto según las preferencias y presupuesto del usuario.

## ✨ Características Principales

### 🧠 Sistema Híbrido de Recomendación

- **Content-Based Filtering**: Compara vinos por características objetivas
- **Collaborative Filtering**: Aprende de patrones de usuarios similares
- **Machine Learning**: Random Forest entrenado con datos reales

### 🎨 Interfaz Intuitiva

- **Búsqueda por presupuesto**: Rango mínimo y máximo personalizable
- **Filtrado por calidad**: Rating mínimo deseado
- **Selección de ocasión**: Romántica, fiesta, regalo, cena especial
- **Preferencias de gusto**: Equilibrado, premium, económico, popular

### 📊 Datos Actualizados

- **Fuente**: Scraping automatizado de Vivino
- **Información completa**: Precios, ratings, reviews, bodegas, regiones
- **Enlaces directos**: Acceso directo a las páginas de Vivino

## 🚀 Instalación y Configuración

### 1. Requisitos Previos

```bash
# Activar entorno virtual
wine_env\Scripts\activate

# Verificar instalación de dependencias
python run_sommelier.py
```

### 2. Entrenar el Modelo

```bash
# Ejecutar el notebook de entrenamiento
jupyter notebook spanish_wine_dataset_classification.ipynb
```

### 3. Ejecutar la Aplicación

```bash
# Iniciar el servidor
python app_sommelier.py

# Abrir en navegador
http://127.0.0.1:5000
```

## 📁 Estructura del Proyecto

```
Wine-IA-Web/
├── app_sommelier.py              # Aplicación Flask principal
├── run_sommelier.py              # Script de verificación
├── templates/
│   ├── sommelier_index.html      # Página principal
│   └── sommelier_about.html      # Información del sistema
├── static/style/
│   └── sommelier.css             # Estilos específicos
├── datos_scraping/
│   └── vivino_scraping_completo_*.csv  # Datos de vinos
└── modelos generados/
    ├── modelo_random_forest_vivino.pkl
    ├── scaler_vivino.pkl
    └── label_encoder_vivino.pkl
```

## 🔧 API Endpoints

### Página Principal

```
GET  /                 # Formulario de búsqueda
POST /                 # Procesar recomendaciones
```

### Información

```
GET  /about           # Detalles técnicos del modelo
```

### API REST

```
GET  /api/vinos                    # Lista completa de vinos
GET  /api/recomendar?parametros    # Recomendaciones personalizadas
```

### Parámetros de API

```
precio_min=15         # Precio mínimo en euros
precio_max=35         # Precio máximo en euros
rating_min=4.1        # Rating mínimo deseado
```

## 🎯 Casos de Uso

### 1. Usuario Casual

- **Presupuesto**: 15€ - 25€
- **Rating**: 4.0+
- **Ocasión**: Uso general
- **Resultado**: Vinos equilibrados con buena relación calidad-precio

### 2. Ocasión Especial

- **Presupuesto**: 30€ - 50€
- **Rating**: 4.15+
- **Ocasión**: Cena romántica
- **Resultado**: Vinos premium para momentos especiales

### 3. Regalo Corporativo

- **Presupuesto**: 25€ - 40€
- **Rating**: 4.1+
- **Ocasión**: Regalo
- **Resultado**: Vinos reconocidos y bien valorados

## 🧪 Tecnologías Utilizadas

### Backend

- **Python 3.12**: Lenguaje principal
- **Flask**: Framework web
- **Scikit-learn**: Machine Learning
- **Pandas**: Procesamiento de datos
- **NumPy**: Cálculos numéricos

### Frontend

- **HTML5 + CSS3**: Estructura y estilos
- **Bootstrap 5**: Framework responsivo
- **JavaScript**: Interactividad
- **Font Awesome**: Iconografía

### Datos

- **Vivino API**: Fuente de datos
- **Beautiful Soup**: Web scraping
- **Selenium**: Automatización de navegador

## 📊 Métricas del Modelo

| Métrica              | Valor                     |
| -------------------- | ------------------------- |
| **Accuracy**         | 100% (conjunto de prueba) |
| **Algoritmo**        | Random Forest             |
| **Características**  | 10 variables              |
| **Dataset**          | 24 vinos españoles        |
| **Rango de precios** | 10.90€ - 43.95€           |
| **Rango de ratings** | 4.11 - 4.19               |

## 🔍 Variables Más Importantes

1. **Rating** (33.1%) - Factor más determinante
2. **Número de reviews** (19.1%) - Popularidad
3. **Posición en Vivino** (11.2%) - Ranking
4. **Precio** (9.3%) - Valor económico
5. **Popularidad** (7.7%) - Reconocimiento

## ⚠️ Limitaciones

### Datos

- **Alcance geográfico**: Solo vinos españoles
- **Fuente única**: Limitado a Vivino
- **Tamaño del dataset**: Dataset relativamente pequeño
- **Temporalidad**: Datos específicos de julio 2025

### Modelo

- **Gustos subjetivos**: Las preferencias varían personalmente
- **Precios dinámicos**: Los precios cambian constantemente
- **Disponibilidad**: No garantiza stock local

## 🔮 Futuras Mejoras

### Expansión de Datos

- [ ] Incluir vinos de otras regiones
- [ ] Integrar múltiples fuentes de datos
- [ ] Análisis de sentimiento en reviews
- [ ] Datos de maridaje gastronómico

### Funcionalidades

- [ ] Sistema de usuarios y favoritos
- [ ] Historial de recomendaciones
- [ ] Notificaciones de ofertas
- [ ] Comparador de vinos

### Modelo

- [ ] Algoritmos más avanzados (Deep Learning)
- [ ] Recomendaciones colaborativas reales
- [ ] Personalización por perfil de usuario
- [ ] Predicción de tendencias

## 🤝 Contribuciones

Este proyecto forma parte de un sistema educativo de Machine Learning aplicado al mundo del vino. Las contribuciones son bienvenidas para:

- Mejorar el algoritmo de recomendación
- Expandir la base de datos
- Optimizar la interfaz de usuario
- Agregar nuevas funcionalidades

## 📄 Licencia

Proyecto educativo desarrollado como parte del curso de Inteligencia Artificial aplicada.

---

**Desarrollado con ❤️ y 🍷 por cegusquiza - Julio 2025**

_"El mejor vino es aquel que se adapta perfectamente a tu momento y presupuesto"_
