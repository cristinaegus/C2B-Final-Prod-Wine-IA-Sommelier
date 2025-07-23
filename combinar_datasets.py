#!/usr/bin/env python3
"""
Script para combinar el dataset de vinos blancos con el dataset existente de tintos
Crear un dataset balanceado con tintos y blancos
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def combinar_datasets():
    """
    Combinar dataset de tintos existente con el nuevo dataset de blancos
    """
    print("🍷 COMBINANDO DATASETS DE VINOS TINTOS Y BLANCOS")
    print("=" * 60)
    
    # Cargar dataset de tintos (ultra limpio)
    try:
        df_tintos = pd.read_csv('datos_scraping/resumen_scraping_completo_20250716_130237_limpio_20250717_113049_ultra_limpio.csv')
        print(f"✅ Dataset de tintos cargado: {len(df_tintos)} vinos")
    except Exception as e:
        print(f"❌ Error cargando tintos: {e}")
        return
    
    # Cargar dataset de blancos generado
    try:
        # Buscar el archivo más reciente de blancos
        archivos_blancos = []
        for archivo in os.listdir('datos_scraping'):
            if archivo.startswith('vinos_blancos_generados_') and archivo.endswith('.csv'):
                archivos_blancos.append(archivo)
        
        if not archivos_blancos:
            print("❌ No se encontró dataset de vinos blancos")
            return
        
        archivo_blancos = max(archivos_blancos)
        df_blancos = pd.read_csv(f'datos_scraping/{archivo_blancos}')
        print(f"✅ Dataset de blancos cargado: {len(df_blancos)} vinos")
        print(f"   📁 Archivo: {archivo_blancos}")
        
    except Exception as e:
        print(f"❌ Error cargando blancos: {e}")
        return
    
    # Verificar columnas comunes
    print(f"\n🔍 ANÁLISIS DE COMPATIBILIDAD:")
    columnas_tintos = set(df_tintos.columns)
    columnas_blancos = set(df_blancos.columns)
    
    columnas_comunes = columnas_tintos.intersection(columnas_blancos)
    columnas_solo_tintos = columnas_tintos - columnas_blancos
    columnas_solo_blancos = columnas_blancos - columnas_tintos
    
    print(f"   📊 Columnas comunes: {len(columnas_comunes)}")
    print(f"   📊 Solo en tintos: {len(columnas_solo_tintos)}")
    print(f"   📊 Solo en blancos: {len(columnas_solo_blancos)}")
    
    if columnas_solo_tintos:
        print(f"   📋 Columnas solo en tintos: {list(columnas_solo_tintos)[:5]}")
    
    if columnas_solo_blancos:
        print(f"   📋 Columnas solo en blancos: {list(columnas_solo_blancos)[:5]}")
    
    # Armonizar datasets - agregar columnas faltantes
    print(f"\n🔧 ARMONIZANDO DATASETS:")
    
    # Agregar columnas faltantes a blancos
    for col in columnas_solo_tintos:
        df_blancos[col] = np.nan
        print(f"   ➕ Agregada columna '{col}' a blancos")
    
    # Agregar columnas faltantes a tintos
    for col in columnas_solo_blancos:
        df_tintos[col] = np.nan
        print(f"   ➕ Agregada columna '{col}' a tintos")
    
    # Asegurar que los tintos tengan tipo_vino = 'Tinto'
    df_tintos['tipo_vino'] = df_tintos['tipo_vino'].fillna('Tinto')
    
    # Reordenar columnas para que sean consistentes
    columnas_ordenadas = sorted(set(df_tintos.columns).union(set(df_blancos.columns)))
    df_tintos = df_tintos.reindex(columns=columnas_ordenadas)
    df_blancos = df_blancos.reindex(columns=columnas_ordenadas)
    
    # Combinar datasets
    print(f"\n🔄 COMBINANDO DATASETS:")
    df_combinado = pd.concat([df_tintos, df_blancos], ignore_index=True)
    
    print(f"   ✅ Dataset combinado: {len(df_combinado)} vinos")
    print(f"   🔴 Tintos: {len(df_tintos)} vinos")
    print(f"   ⚪ Blancos: {len(df_blancos)} vinos")
    
    # Análisis del dataset combinado
    print(f"\n📊 ANÁLISIS DEL DATASET COMBINADO:")
    
    # Tipos de vino
    tipos_vino = df_combinado['tipo_vino'].value_counts()
    print(f"   🍷 Distribución por tipo:")
    for tipo, cantidad in tipos_vino.items():
        porcentaje = (cantidad / len(df_combinado)) * 100
        emoji = "🔴" if tipo == "Tinto" else "⚪" if tipo == "Blanco" else "🍷"
        print(f"      {emoji} {tipo}: {cantidad} vinos ({porcentaje:.1f}%)")
    
    # Estadísticas de precios
    if 'precio_eur' in df_combinado.columns:
        precios_validos = df_combinado['precio_eur'].dropna()
        if len(precios_validos) > 0:
            print(f"   💰 Precios:")
            print(f"      • Promedio: €{precios_validos.mean():.2f}")
            print(f"      • Rango: €{precios_validos.min():.2f} - €{precios_validos.max():.2f}")
            
            # Por tipo
            for tipo in ['Tinto', 'Blanco']:
                tipo_data = df_combinado[df_combinado['tipo_vino'] == tipo]['precio_eur'].dropna()
                if len(tipo_data) > 0:
                    print(f"      • {tipo}: €{tipo_data.mean():.2f} (promedio)")
    
    # Estadísticas de ratings
    if 'rating' in df_combinado.columns:
        ratings_validos = df_combinado['rating'].dropna()
        if len(ratings_validos) > 0:
            print(f"   ⭐ Ratings:")
            print(f"      • Promedio: {ratings_validos.mean():.2f}")
            print(f"      • Rango: {ratings_validos.min():.2f} - {ratings_validos.max():.2f}")
    
    # Guardar dataset combinado
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"datos_scraping/dataset_vinos_combinado_{timestamp}.csv"
    
    df_combinado.to_csv(nombre_archivo, index=False, encoding='utf-8')
    
    print(f"\n💾 DATASET COMBINADO GUARDADO:")
    print(f"   📁 Archivo: {nombre_archivo}")
    print(f"   📊 Total de vinos: {len(df_combinado)}")
    
    # Crear también una versión optimizada sin valores nulos críticos
    print(f"\n🧹 CREANDO VERSIÓN ULTRA LIMPIA:")
    
    # Eliminar registros con valores nulos en columnas críticas
    columnas_criticas = ['precio_eur', 'bodega', 'año', 'tipo_vino']
    df_ultra_limpio = df_combinado.dropna(subset=columnas_criticas)
    
    nombre_archivo_limpio = f"datos_scraping/dataset_vinos_combinado_ultra_limpio_{timestamp}.csv"
    df_ultra_limpio.to_csv(nombre_archivo_limpio, index=False, encoding='utf-8')
    
    print(f"   📁 Archivo ultra limpio: {nombre_archivo_limpio}")
    print(f"   📊 Vinos ultra limpios: {len(df_ultra_limpio)}")
    print(f"   🗑️ Registros eliminados: {len(df_combinado) - len(df_ultra_limpio)}")
    
    # Análisis final del dataset ultra limpio
    tipos_ultra = df_ultra_limpio['tipo_vino'].value_counts()
    print(f"\n🎯 DATASET ULTRA LIMPIO - DISTRIBUCIÓN FINAL:")
    for tipo, cantidad in tipos_ultra.items():
        porcentaje = (cantidad / len(df_ultra_limpio)) * 100
        emoji = "🔴" if tipo == "Tinto" else "⚪" if tipo == "Blanco" else "🍷"
        print(f"   {emoji} {tipo}: {cantidad} vinos ({porcentaje:.1f}%)")
    
    print(f"\n🎉 PROCESO COMPLETADO EXITOSAMENTE")
    print(f"   📈 Dataset balanceado creado con {len(df_ultra_limpio)} vinos")
    print(f"   ⚖️ Proporción tintos/blancos más equilibrada")
    
    return nombre_archivo_limpio

if __name__ == "__main__":
    archivo_final = combinar_datasets()
