# 🚀 Guía de Puertos de las Aplicaciones

## 📊 Aplicaciones Disponibles

### 🍷 Aplicación Original - Clasificador de Calidad

- **Archivo**: `app_wine.py`
- **Puerto**: `5000`
- **URL**: http://127.0.0.1:5000
- **Función**: Clasifica la calidad del vino basándose en características químicas
- **Datos**: Dataset winequality-red.csv
- **Formulario**: 11 parámetros químicos (acidez, sulfatos, alcohol, etc.)

### 🧠 Sommelier Inteligente - Recomendador de Vinos

- **Archivo**: `app_sommelier.py`
- **Puerto**: `5001`
- **URL**: http://127.0.0.1:5001
- **Función**: Recomienda vinos españoles basándose en presupuesto y ocasión
- **Datos**: Vivino scraping data (vinos reales)
- **Formulario**: Presupuesto, rating, ocasión, preferencias

## 🔧 Comandos de Ejecución

### Ejecutar Clasificador Original

```bash
cd "c:\Users\Dell\PyhtonIA\Wine-IA-Web"
python app_wine.py
# Disponible en: http://127.0.0.1:5000
```

### Ejecutar Sommelier Inteligente

```bash
cd "c:\Users\Dell\PyhtonIA\Wine-IA-Web"
python app_sommelier.py
# Disponible en: http://127.0.0.1:5001
```

### Ejecutar Ambas Aplicaciones (Paralelo)

```bash
# Terminal 1: Clasificador
python app_wine.py

# Terminal 2: Sommelier
python app_sommelier.py
```

## 📋 Diferencias Principales

| Característica | Clasificador (5000)         | Sommelier (5001)            |
| -------------- | --------------------------- | --------------------------- |
| **Propósito**  | Análisis químico            | Recomendación personalizada |
| **Entrada**    | 11 variables químicas       | Presupuesto + preferencias  |
| **Salida**     | Calidad 3-8/10              | Lista de vinos recomendados |
| **Dataset**    | Laboratorio (1599 muestras) | Vivino real (24 vinos)      |
| **Modelo**     | Random Forest químico       | Random Forest comercial     |
| **Usuario**    | Enólogos/Científicos        | Consumidores finales        |

## 🎯 Casos de Uso

### Usar Clasificador (Puerto 5000) cuando:

- ✅ Tienes datos químicos del vino
- ✅ Quieres evaluar calidad objetiva
- ✅ Necesitas análisis de laboratorio
- ✅ Investigación enológica

### Usar Sommelier (Puerto 5001) cuando:

- ✅ Quieres comprar vino
- ✅ Tienes un presupuesto específico
- ✅ Buscas para una ocasión especial
- ✅ Quieres recomendaciones personalizadas

## 🚦 Estado de Servidores

Para verificar qué aplicaciones están corriendo:

```bash
# Verificar puerto 5000 (Clasificador)
curl http://127.0.0.1:5000

# Verificar puerto 5001 (Sommelier)
curl http://127.0.0.1:5001
```

## 📁 Archivos de Configuración

- **Clasificador**: Configuración directa en `app_wine.py`
- **Sommelier**: Configuración centralizada en `config_sommelier.py`

---

**Recomendación**: Usa ambas aplicaciones según tu necesidad específica. Son complementarias, no excluyentes.
