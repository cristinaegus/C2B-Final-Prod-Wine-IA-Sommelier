#!/usr/bin/env python3
"""
🍷 Sommelier Inteligente - Instrucciones de Ejecución
=====================================================

Este script contiene las instrucciones para ejecutar el Sommelier Inteligente
basado en los datos del scraping de Vivino.

REQUISITOS PREVIOS:
==================
1. Haber ejecutado el notebook 'spanish_wine_dataset_classification.ipynb'
2. Que existan los archivos del modelo:
   - modelo_random_forest_vivino.pkl
   - scaler_vivino.pkl
   - label_encoder_vivino.pkl
3. Que exista al menos un archivo 'vivino_scraping_completo_*.csv' en 'datos_scraping/'

INSTRUCCIONES DE EJECUCIÓN:
==========================
1. Abrir terminal en la carpeta del proyecto
2. Activar el entorno virtual wine_env:
   > wine_env\Scripts\activate
3. Ejecutar la aplicación Sommelier:
   > python app_sommelier.py
4. Abrir navegador en: http://127.0.0.1:5000

FUNCIONALIDADES:
===============
✅ Recomendación personalizada de vinos según presupuesto
✅ Filtrado por rating mínimo y ocasión
✅ Búsqueda en datos reales de Vivino
✅ Información detallada de cada vino recomendado
✅ Enlaces directos a Vivino
✅ API REST para integraciones

ENDPOINTS DISPONIBLES:
=====================
/ (GET/POST)          - Página principal del Sommelier
/about (GET)          - Información del modelo y tecnologías
/api/vinos (GET)      - API con lista de vinos disponibles
/api/recomendar (GET) - API de recomendaciones con parámetros

PARÁMETROS DE LA API:
====================
/api/recomendar?precio_min=15&precio_max=35&rating_min=4.1

DIFERENCIAS CON app_wine.py:
===========================
- app_wine.py: Modelo original de clasificación de calidad (11 parámetros químicos)
- app_sommelier.py: Sistema de recomendación basado en datos de Vivino (presupuesto, ocasión, gusto)

ARCHIVOS CLAVE:
===============
- app_sommelier.py: Aplicación Flask principal
- templates/sommelier_index.html: Página principal
- templates/sommelier_about.html: Página de información
- static/style/sommelier.css: Estilos específicos
- datos_scraping/vivino_scraping_completo_*.csv: Datos de vinos

🚀 ¡Listo para usar el Sommelier Inteligente!
"""

# Importar librerías necesarias para verificar instalación
try:
    import flask
    import pandas as pd
    import numpy as np
    import sklearn
    print("✅ Todas las librerías están instaladas correctamente")
except ImportError as e:
    print(f"❌ Error: Falta instalar {e.name}")
    print("💡 Ejecute: pip install flask pandas numpy scikit-learn")

# Verificar archivos necesarios
import os
import glob

print("\n🔍 Verificando archivos necesarios...")

# Verificar modelos
modelos_necesarios = [
    'modelo_random_forest_vivino.pkl',
    'scaler_vivino.pkl', 
    'label_encoder_vivino.pkl'
]

for modelo in modelos_necesarios:
    if os.path.exists(modelo):
        print(f"✅ {modelo}")
    else:
        print(f"❌ {modelo} - Ejecute el notebook primero")

# Verificar datos de scraping
archivos_scraping = glob.glob('datos_scraping/vivino_scraping_completo_*.csv')
if archivos_scraping:
    archivo_mas_reciente = max(archivos_scraping, key=os.path.getctime)
    print(f"✅ Datos de scraping encontrados: {archivo_mas_reciente}")
else:
    print("❌ No se encontraron archivos de scraping completo")

print("\n🍷 Para ejecutar el Sommelier Inteligente:")
print("   python app_sommelier.py")
print("   Luego abrir: http://127.0.0.1:5001")
