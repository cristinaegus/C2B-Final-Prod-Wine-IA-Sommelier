#!/usr/bin/env python3
"""
Resumen Completo de Scraping de Vivino
Script para analizar y resumir todos los datos extraídos de Vivino
"""

import pandas as pd
import os
from datetime import datetime
import re

def analizar_archivos_scraping():
    """Analiza todos los archivos CSV de scraping generados"""
    
    carpeta = "datos_scraping"
    archivos_csv = []
    
    # Buscar todos los archivos CSV
    for archivo in os.listdir(carpeta):
        if archivo.endswith('.csv') and 'vivino' in archivo.lower():
            archivos_csv.append(os.path.join(carpeta, archivo))
    
    print("🍷 RESUMEN COMPLETO DE SCRAPING DE VIVINO")
    print("=" * 60)
    print(f"🕐 Análisis realizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Carpeta analizada: {carpeta}")
    print(f"📄 Archivos CSV encontrados: {len(archivos_csv)}")
    
    # Análisis por archivo
    print(f"\n📊 ANÁLISIS POR ARCHIVO:")
    print("-" * 60)
    
    datos_totales = []
    resumen_archivos = []
    
    for archivo in sorted(archivos_csv):
        try:
            nombre_archivo = os.path.basename(archivo)
            df = pd.read_csv(archivo, encoding='utf-8')
            
            # Información básica del archivo
            num_filas = len(df)
            columnas = list(df.columns)
            
            # Análisis de precios
            if 'precio_eur' in df.columns:
                precios = df['precio_eur'].dropna()
                precio_min = precios.min() if len(precios) > 0 else None
                precio_max = precios.max() if len(precios) > 0 else None
                precio_promedio = precios.mean() if len(precios) > 0 else None
            else:
                precio_min = precio_max = precio_promedio = None
            
            # Análisis de ratings
            if 'rating' in df.columns:
                ratings = df['rating'].dropna()
                rating_promedio = ratings.mean() if len(ratings) > 0 else None
                rating_min = ratings.min() if len(ratings) > 0 else None
                rating_max = ratings.max() if len(ratings) > 0 else None
            else:
                rating_promedio = rating_min = rating_max = None
            
            # Análisis de regiones
            if 'region' in df.columns:
                regiones = df['region'].dropna().value_counts()
                top_region = regiones.index[0] if len(regiones) > 0 else None
                num_regiones = len(regiones)
            else:
                top_region = None
                num_regiones = 0
            
            # Análisis de años
            if 'año' in df.columns:
                años = df['año'].dropna()
                año_min = años.min() if len(años) > 0 else None
                año_max = años.max() if len(años) > 0 else None
            else:
                año_min = año_max = None
            
            print(f"\n📄 {nombre_archivo}")
            print(f"   🍷 Total vinos: {num_filas}")
            print(f"   📊 Columnas: {len(columnas)}")
            
            if precio_min is not None:
                print(f"   💶 Precios: €{precio_min:.2f} - €{precio_max:.2f} (Promedio: €{precio_promedio:.2f})")
            
            if rating_promedio is not None:
                print(f"   ⭐ Ratings: {rating_min:.1f} - {rating_max:.1f} (Promedio: {rating_promedio:.2f})")
            
            if top_region:
                print(f"   🌍 Regiones: {num_regiones} diferentes (Top: {top_region})")
            
            if año_min is not None:
                print(f"   📅 Años: {año_min} - {año_max}")
            
            # Guardar datos para análisis global
            df['archivo_origen'] = nombre_archivo
            datos_totales.append(df)
            
            resumen_archivos.append({
                'archivo': nombre_archivo,
                'vinos': num_filas,
                'precio_min': precio_min,
                'precio_max': precio_max,
                'precio_promedio': precio_promedio,
                'rating_promedio': rating_promedio,
                'regiones': num_regiones,
                'año_min': año_min,
                'año_max': año_max
            })
            
        except Exception as e:
            print(f"   ❌ Error procesando {nombre_archivo}: {e}")
    
    # Análisis global combinado
    if datos_totales:
        print(f"\n🌟 ANÁLISIS GLOBAL COMBINADO:")
        print("-" * 60)
        
        # Combinar todos los datos
        df_global = pd.concat(datos_totales, ignore_index=True)
        
        # Estadísticas globales
        total_vinos = len(df_global)
        archivos_procesados = len(datos_totales)
        
        print(f"📊 Total de vinos combinados: {total_vinos}")
        print(f"📁 Archivos procesados: {archivos_procesados}")
        
        # Análisis de URLs únicas (evitar duplicados)
        if 'url' in df_global.columns:
            urls_unicas = df_global['url'].dropna().nunique()
            print(f"🔗 Vinos únicos (por URL): {urls_unicas}")
            duplicados = total_vinos - urls_unicas
            if duplicados > 0:
                print(f"⚠️ Duplicados detectados: {duplicados}")
        
        # Análisis de precios global
        if 'precio_eur' in df_global.columns:
            precios_globales = df_global['precio_eur'].dropna()
            if len(precios_globales) > 0:
                print(f"\n💶 ANÁLISIS DE PRECIOS GLOBAL:")
                print(f"   Vinos con precio: {len(precios_globales)} ({len(precios_globales)/total_vinos*100:.1f}%)")
                print(f"   Rango completo: €{precios_globales.min():.2f} - €{precios_globales.max():.2f}")
                print(f"   Precio promedio: €{precios_globales.mean():.2f}")
                print(f"   Precio mediano: €{precios_globales.median():.2f}")
                
                # Distribución por rangos de precio
                rangos = [
                    (0, 15, "Económicos €0-15"),
                    (15, 30, "Medios €15-30"),
                    (30, 50, "Premium €30-50"),
                    (50, 100, "Lujo €50-100"),
                    (100, 1000, "Ultra-premium €100+")
                ]
                
                print(f"   📊 Distribución por rangos:")
                for min_precio, max_precio, etiqueta in rangos:
                    count = len(precios_globales[(precios_globales >= min_precio) & (precios_globales < max_precio)])
                    if count > 0:
                        porcentaje = count / len(precios_globales) * 100
                        print(f"      {etiqueta}: {count} vinos ({porcentaje:.1f}%)")
        
        # Análisis de ratings global
        if 'rating' in df_global.columns:
            ratings_globales = df_global['rating'].dropna()
            if len(ratings_globales) > 0:
                print(f"\n⭐ ANÁLISIS DE RATINGS GLOBAL:")
                print(f"   Vinos con rating: {len(ratings_globales)} ({len(ratings_globales)/total_vinos*100:.1f}%)")
                print(f"   Rating promedio: {ratings_globales.mean():.2f}")
                print(f"   Rango: {ratings_globales.min():.1f} - {ratings_globales.max():.1f}")
                
                # Distribución por calidad
                excelentes = len(ratings_globales[ratings_globales >= 4.3])
                muy_buenos = len(ratings_globales[(ratings_globales >= 4.0) & (ratings_globales < 4.3)])
                buenos = len(ratings_globales[(ratings_globales >= 3.5) & (ratings_globales < 4.0)])
                
                print(f"   📊 Distribución por calidad:")
                print(f"      Excelentes (4.3+): {excelentes} vinos ({excelentes/len(ratings_globales)*100:.1f}%)")
                print(f"      Muy buenos (4.0-4.2): {muy_buenos} vinos ({muy_buenos/len(ratings_globales)*100:.1f}%)")
                print(f"      Buenos (3.5-3.9): {buenos} vinos ({buenos/len(ratings_globales)*100:.1f}%)")
        
        # Análisis de regiones global
        if 'region' in df_global.columns:
            regiones_globales = df_global['region'].dropna().value_counts()
            if len(regiones_globales) > 0:
                print(f"\n🌍 ANÁLISIS DE REGIONES GLOBAL:")
                print(f"   Total regiones diferentes: {len(regiones_globales)}")
                print(f"   Top 10 regiones:")
                for i, (region, count) in enumerate(regiones_globales.head(10).items(), 1):
                    porcentaje = count / len(df_global['region'].dropna()) * 100
                    print(f"      {i:2d}. {region}: {count} vinos ({porcentaje:.1f}%)")
        
        # Análisis de años global
        if 'año' in df_global.columns:
            años_globales = df_global['año'].dropna()
            if len(años_globales) > 0:
                print(f"\n📅 ANÁLISIS DE AÑOS GLOBAL:")
                print(f"   Rango de años: {años_globales.min()} - {años_globales.max()}")
                años_count = años_globales.value_counts().sort_index(ascending=False)
                print(f"   Top años más frecuentes:")
                for año, count in años_count.head(8).items():
                    porcentaje = count / len(años_globales) * 100
                    print(f"      {año}: {count} vinos ({porcentaje:.1f}%)")
        
        # Análisis de bodegas
        if 'bodega' in df_global.columns:
            bodegas = df_global['bodega'].dropna().value_counts()
            if len(bodegas) > 0:
                print(f"\n🏭 ANÁLISIS DE BODEGAS:")
                print(f"   Total bodegas diferentes: {len(bodegas)}")
                print(f"   Top 8 bodegas:")
                for i, (bodega, count) in enumerate(bodegas.head(8).items(), 1):
                    if len(bodega) > 30:
                        bodega = bodega[:27] + "..."
                    print(f"      {i}. {bodega}: {count} vinos")
        
        # Guardar resumen combinado
        archivo_resumen = os.path.join(carpeta, f"resumen_scraping_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        df_global.to_csv(archivo_resumen, index=False, encoding='utf-8')
        print(f"\n💾 Resumen combinado guardado en: {archivo_resumen}")
    
    print(f"\n" + "=" * 60)
    print("✅ ANÁLISIS COMPLETO FINALIZADO")
    print("📊 Datos listos para uso en el modelo de ML")
    print("🍷 ¡Scraping de Vivino completado exitosamente!")

if __name__ == "__main__":
    analizar_archivos_scraping()
