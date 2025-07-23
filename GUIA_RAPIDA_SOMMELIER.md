# 🍷 Sommelier Inteligente - Guía Rápida

## 🚀 Inicio Rápido

### 1. Activar Entorno Virtual

```bash
wine_env\Scripts\activate
```

### 2. Verificar y Ejecutar

```bash
# Opción 1: Script automático (RECOMENDADO)
python deploy_sommelier.py

# Opción 2: Ejecución directa
python app_sommelier.py
```

### 3. Abrir en Navegador

```
http://127.0.0.1:5000
```

## 🎯 Uso del Sistema

### Búsqueda Básica

1. **Presupuesto**: Establece rango de precios (€)
2. **Rating mínimo**: Calidad deseada (3.8 - 5.0)
3. **Ocasión**: Selecciona el contexto de uso
4. **Preferencias**: Estilo de vino preferido

### Filtros Avanzados

- **API REST**: `/api/recomendar?precio_min=15&precio_max=35&rating_min=4.1`
- **JSON Response**: Datos estructurados para integraciones

## 📁 Archivos Importantes

| Archivo                      | Descripción                     |
| ---------------------------- | ------------------------------- |
| `app_sommelier.py`           | Aplicación Flask principal      |
| `config_sommelier.py`        | Configuración centralizada      |
| `deploy_sommelier.py`        | Script de despliegue automático |
| `templates/sommelier_*.html` | Interfaz web                    |
| `static/style/sommelier.css` | Estilos personalizados          |

## 🔧 Resolución de Problemas

### Error: "No se encontraron archivos CSV"

```bash
# Ejecutar scraping para generar datos
python datos.py
```

### Error: "Modelo no encontrado"

```bash
# Entrenar modelo desde notebook
jupyter notebook spanish_wine_dataset_classification.ipynb
```

### Error: "Puerto 5000 ocupado"

```python
# Cambiar puerto en config_sommelier.py
PORT = 8080
```

## 🌐 URLs del Sistema

- **Inicio**: `http://127.0.0.1:5001/`
- **Información**: `http://127.0.0.1:5001/about`
- **API Vinos**: `http://127.0.0.1:5001/api/vinos`
- **API Recomendaciones**: `http://127.0.0.1:5001/api/recomendar`

## 💡 Consejos de Uso

### Para Principiantes

- Presupuesto: €15-25
- Rating: 4.0+
- Ocasión: General

### Para Ocasiones Especiales

- Presupuesto: €30-50
- Rating: 4.15+
- Ocasión: Romántica/Especial

### Para Regalos

- Presupuesto: €25-40
- Rating: 4.1+
- Ocasión: Regalo

## 📊 Datos del Sistema

- **Fuente**: Vivino (scraping automatizado)
- **Algoritmo**: Random Forest
- **Precisión**: 100% en conjunto de prueba
- **Variables**: 10 características por vino
- **Actualización**: Manual (ejecutar scraping)

## 🔒 Seguridad

- Servidor solo accesible localmente por defecto
- No se almacenan datos de usuario
- Configuración en archivos locales
- Sin autenticación requerida

## 🔧 ¿Qué es la Paralelización de Tareas Computacionales?

La **paralelización de tareas computacionales** significa ejecutar múltiples operaciones al mismo tiempo en lugar de una por una, aprovechando varios núcleos del procesador o hilos para acelerar el procesamiento.

### 🔄 **¿Qué es la Paralelización?**

En lugar de hacer esto (secuencial):
```
Tarea 1 → Tarea 2 → Tarea 3 → Tarea 4
```

La paralelización hace esto (paralelo):
```
Tarea 1 ┐
Tarea 2 ├─ Al mismo tiempo
Tarea 3 ┤
Tarea 4 ┘
```

### 🍷 **En el contexto de Wine IA:**

#### **1. Entrenamiento de Modelos ML**
```python
# Sin paralelización: 1 modelo a la vez
for model in models:
    train_model(model)  # 30 segundos cada uno = 5 minutos total

# Con paralelización: varios modelos simultáneamente  
joblib.Parallel(n_jobs=4)(
    joblib.delayed(train_model)(model) for model in models
)  # 30 segundos total
```

#### **2. Procesamiento de Datos**
```python
# Procesar 1000 vinos uno por uno vs. 100 a la vez en 10 grupos paralelos
```

#### **3. Búsquedas y Filtros**
```python
# Buscar en múltiples fuentes de datos simultáneamente
# Calcular recomendaciones para varios usuarios a la vez
```

### ⚡ **Ventajas:**

- **🚀 Velocidad**: Tareas que tomaban 10 minutos ahora toman 2-3 minutos
- **💪 Eficiencia**: Usa todo el poder del procesador
- **📈 Escalabilidad**: Puede manejar más usuarios y datos

### 🛠️ **Cómo joblib lo hace:**

```python
# Ejemplo: Entrenar 5 modelos en paralelo
from joblib import Parallel, delayed

def entrenar_modelo(parametros):
    # Entrenar modelo con estos parámetros
    return modelo_entrenado

# Ejecutar en paralelo usando 4 núcleos del CPU
modelos = Parallel(n_jobs=4)(
    delayed(entrenar_modelo)(params) for params in lista_parametros
)
```

**En resumen**: paralelización = hacer varias cosas a la vez = más rápido = mejor experiencia de usuario 🚀

---

**¿Necesitas ayuda?** Revisa `README_SOMMELIER.md` para documentación completa.


