#!/usr/bin/env python3
"""
Script para analizar los tipos de vino disponibles en el dataset
"""

import pandas as pd
import numpy as np
from collections import Counter

def analizar_tipos_vino():
    """
    Analiza los tipos de vino disponibles en el dataset ultra limpio
    """
    print("🍷 ANÁLISIS DE TIPOS DE VINO EN EL DATASET")
    print("=" * 60)
    
    # Cargar el dataset ultra limpio
    try:
        df = pd.read_csv('datos_scraping/resumen_scraping_completo_20250716_130237_limpio_20250717_113049_ultra_limpio.csv')
        print(f"✅ Dataset cargado: {len(df)} vinos")
    except Exception as e:
        print(f"❌ Error cargando dataset: {e}")
        return
    
    # Verificar si existe la columna tipo_vino
    if 'tipo_vino' not in df.columns:
        print("❌ La columna 'tipo_vino' no existe en el dataset")
        print(f"📋 Columnas disponibles: {list(df.columns)}")
        return
    
    # Análisis de tipos de vino
    print(f"\n📊 ANÁLISIS DE LA COLUMNA 'tipo_vino':")
    
    # Contar valores nulos
    nulos = df['tipo_vino'].isnull().sum()
    print(f"   ⚠️ Valores nulos: {nulos} ({nulos/len(df)*100:.1f}%)")
    
    # Contar tipos de vino disponibles
    tipos_vino = df['tipo_vino'].value_counts()
    print(f"\n🍷 TIPOS DE VINO DISPONIBLES:")
    print(f"   📈 Total de tipos únicos: {len(tipos_vino)}")
    
    for i, (tipo, cantidad) in enumerate(tipos_vino.items(), 1):
        porcentaje = (cantidad / len(df)) * 100
        emoji = "🔴" if "tinto" in str(tipo).lower() else "⚪" if "blanco" in str(tipo).lower() else "🌸" if "rosado" in str(tipo).lower() else "🍷"
        print(f"   {emoji} {i}. {tipo}: {cantidad} vinos ({porcentaje:.1f}%)")
    
    # Mostrar ejemplos de cada tipo
    print(f"\n🔍 EJEMPLOS DETALLADOS POR TIPO:")
    
    for tipo in tipos_vino.index[:5]:  # Top 5 tipos más comunes
        print(f"\n{'='*20} {tipo.upper()} {'='*20}")
        ejemplos = df[df['tipo_vino'] == tipo].head(5)
        
        for j, (_, vino) in enumerate(ejemplos.iterrows(), 1):
            bodega = vino.get('bodega', 'Sin bodega')
            año = vino.get('año', 'Sin año')
            precio = vino.get('precio_eur', 'Sin precio')
            region = vino.get('region', 'Sin región')
            rating = vino.get('rating', 'Sin rating')
            
            print(f"   {j}. 🏭 {bodega}")
            print(f"      📅 Año: {año} | 💰 Precio: €{precio}")
            print(f"      🌍 Región: {region} | ⭐ Rating: {rating}")
            print()
    
    # Análisis adicional de nombres para detectar tipos
    print(f"\n🔬 ANÁLISIS ADICIONAL - DETECCIÓN EN NOMBRES:")
    
    # Buscar palabras clave en nombres y bodegas
    df_nombres = df['bodega'].fillna('') + ' ' + df.get('nombre_completo', '').fillna('')
    
    # Contadores para diferentes tipos
    keywords = {
        'Tinto': ['tinto', 'red', 'garnacha', 'tempranillo', 'cabernet', 'merlot', 'syrah'],
        'Blanco': ['blanco', 'white', 'chardonnay', 'sauvignon blanc', 'albariño', 'verdejo'],
        'Rosado': ['rosado', 'rosé', 'pink'],
        'Espumoso': ['cava', 'champagne', 'espumoso', 'sparkling']
    }
    
    print("   🔍 Detección por palabras clave en nombres/bodegas:")
    for tipo_detectado, palabras in keywords.items():
        contador = 0
        for palabra in palabras:
            contador += df_nombres.str.contains(palabra, case=False, na=False).sum()
        
        emoji = "🔴" if tipo_detectado == "Tinto" else "⚪" if tipo_detectado == "Blanco" else "🌸" if tipo_detectado == "Rosado" else "🥂"
        print(f"   {emoji} {tipo_detectado}: ~{contador} menciones")
    
    # Análisis de regiones típicas
    print(f"\n🌍 ANÁLISIS POR REGIONES (indicativo de tipos):")
    regiones_tipicas = {
        'Ribera del Duero': 'Principalmente Tinto',
        'Rioja': 'Principalmente Tinto',
        'Rías Baixas': 'Principalmente Blanco',
        'Rueda': 'Principalmente Blanco',
        'Cava': 'Espumoso',
        'Campo de Borja': 'Principalmente Tinto',
        'Calatayud': 'Principalmente Tinto'
    }
    
    if 'region' in df.columns:
        regiones = df['region'].value_counts().head(10)
        for region, cantidad in regiones.items():
            tipo_probable = regiones_tipicas.get(region, 'Mixto')
            emoji = "🔴" if "Tinto" in tipo_probable else "⚪" if "Blanco" in tipo_probable else "🥂" if "Espumoso" in tipo_probable else "🍷"
            print(f"   {emoji} {region}: {cantidad} vinos ({tipo_probable})")
    
    # Resumen final
    print(f"\n🎯 RESUMEN FINAL:")
    print(f"   📊 Total de vinos analizados: {len(df)}")
    print(f"   🏷️ Tipos únicos en columna 'tipo_vino': {len(tipos_vino)}")
    print(f"   ✅ Datos disponibles para clasificación: {len(df) - nulos} vinos")
    
    if len(tipos_vino) > 0:
        tipo_principal = tipos_vino.index[0]
        cantidad_principal = tipos_vino.iloc[0]
        print(f"   🏆 Tipo más común: {tipo_principal} ({cantidad_principal} vinos)")

if __name__ == "__main__":
    analizar_tipos_vino()
