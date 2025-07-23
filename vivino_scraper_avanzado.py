#!/usr/bin/env python3
"""
Vivino Scraper Avanzado - Última Versión
Script especializado para scraping completo de Vivino con datos actualizados
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import os
import re
import json
from datetime import datetime
import random

class VivinoScraperAvanzado:
    """Scraper avanzado para Vivino con múltiples estrategias"""
    
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.datos_extraidos = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def configurar_driver(self):
        """Configura el driver de Chrome con opciones optimizadas"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # Opciones de rendimiento
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # User agents rotativos para evitar detección
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            ]
            chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
            
            # Configuraciones adicionales
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Ocultar características de webdriver
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.driver = driver
            print("✅ Driver configurado exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error configurando driver: {e}")
            return False
    
    def crear_carpeta_datos(self):
        """Crea la carpeta de datos si no existe"""
        carpeta = "datos_scraping"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            print(f"📁 Carpeta creada: {carpeta}")
        return carpeta
    
    def scroll_inteligente(self, pausas=3):
        """Realiza scroll inteligente para cargar contenido dinámico"""
        print("📜 Iniciando scroll inteligente para cargar contenido...")
        
        for i in range(pausas):
            # Scroll hacia abajo
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2 + random.uniform(0.5, 1.5))
            
            # Scroll hacia arriba parcial
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
            time.sleep(1)
            
            print(f"   Scroll {i+1}/{pausas} completado")
        
        # Scroll final hacia abajo
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        print("✅ Scroll inteligente completado")
    
    def extraer_datos_vino(self, elemento_texto, url_vino, posicion):
        """Extrae datos detallados de un vino desde el texto"""
        
        vino_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'session_id': self.session_id,
            'posicion': posicion,
            'nombre_completo': elemento_texto,
            'url': url_vino,
            'precio_eur': None,
            'bodega': '',
            'region': '',
            'año': None,
            'rating': None,
            'num_reviews': None,
            'categoria_calidad': '',
            'tipo_vino': '',
            'descuento': None,
            'precio_original': None,
            'disponibilidad': 'Disponible'
        }
        
        # Extraer precio actual
        precio_match = re.search(r'(\d+[,.]?\d*)\s*€', elemento_texto)
        if precio_match:
            try:
                precio = float(precio_match.group(1).replace(',', '.'))
                vino_data['precio_eur'] = precio
            except:
                pass
        
        # Extraer precio original y descuento
        precio_original_match = re.search(r'(\d+[,.]?\d*)\s*€.*?(\d+[,.]?\d*)\s*€', elemento_texto)
        if precio_original_match:
            try:
                precio_original = float(precio_original_match.group(1).replace(',', '.'))
                precio_actual = float(precio_original_match.group(2).replace(',', '.'))
                if precio_original > precio_actual:
                    vino_data['precio_original'] = precio_original
                    vino_data['descuento'] = round(((precio_original - precio_actual) / precio_original) * 100, 1)
            except:
                pass
        
        # Extraer rating y reviews
        rating_pattern = r'(\d+[,.]?\d+)\s*(\d+)\s*valoraciones'
        rating_match = re.search(rating_pattern, elemento_texto)
        if rating_match:
            try:
                rating = float(rating_match.group(1).replace(',', '.'))
                num_reviews = int(rating_match.group(2))
                vino_data['rating'] = rating
                vino_data['num_reviews'] = num_reviews
            except:
                pass
        
        # Extraer año
        año_match = re.search(r'(20\d{2}|19\d{2})', elemento_texto)
        if año_match:
            vino_data['año'] = int(año_match.group(1))
        
        # Extraer región (lista expandida)
        regiones_españa = [
            'España', 'Rioja', 'Ribera del Duero', 'Cataluña', 'Catalunya', 'Madrid',
            'Aragón', 'Castilla', 'Extremadura', 'Campo de Borja', 'Calatayud',
            'Terra Alta', 'Somontano', 'Empordà', 'Cariñena', 'Valdejalón',
            'Jumilla', 'Yecla', 'Bullas', 'Almansa', 'Manchuela', 'La Mancha',
            'Valdepeñas', 'Montilla-Moriles', 'Jerez', 'Manzanilla', 'Málaga',
            'Sierras de Málaga', 'Condado de Huelva', 'Galicia', 'Rías Baixas',
            'Ribeiro', 'Valdeorras', 'Monterrei', 'Asturias', 'Cantabria',
            'País Vasco', 'Euskadi', 'Txakoli', 'Navarra', 'Cava', 'Penedès',
            'Priorat', 'Montsant', 'Costers del Segre', 'Alella', 'Pla de Bages'
        ]
        
        for region in regiones_españa:
            if region in elemento_texto:
                vino_data['region'] = region
                break
        
        # Extraer categoría de calidad
        calidades = [
            'Great Value', 'Good Value', 'Amazing Value', 'Cosecha más antigua',
            'Top Rated', 'Critics Choice', 'Best Value', 'Premium', 'Limited Edition',
            'Organic', 'Biodynamic', 'Sustainable'
        ]
        
        for calidad in calidades:
            if calidad in elemento_texto:
                vino_data['categoria_calidad'] = calidad
                break
        
        # Extraer tipo de vino
        tipos_vino = [
            'Tinto', 'Blanco', 'Rosado', 'Rosé', 'Espumoso', 'Cava', 'Champagne',
            'Dulce', 'Seco', 'Semiseco', 'Generoso', 'Licoroso', 'Crianza',
            'Reserva', 'Gran Reserva', 'Joven'
        ]
        
        for tipo in tipos_vino:
            if tipo in elemento_texto:
                vino_data['tipo_vino'] = tipo
                break
        
        # Extraer bodega (mejorado)
        # Buscar patrones como "Bodega Nombre" o "Nombre Winery"
        bodega_patterns = [
            r'^([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',  # Primer conjunto de palabras
            r'Bodega\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',  # Después de "Bodega"
            r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\s+Winery',  # Antes de "Winery"
        ]
        
        for pattern in bodega_patterns:
            bodega_match = re.search(pattern, elemento_texto)
            if bodega_match:
                posible_bodega = bodega_match.group(1).strip()
                if len(posible_bodega) > 2 and not posible_bodega.isdigit():
                    vino_data['bodega'] = posible_bodega
                    break
        
        # Si no encontró bodega, usar primera palabra significativa
        if not vino_data['bodega']:
            palabras = elemento_texto.split()
            for palabra in palabras[:3]:  # Revisar primeras 3 palabras
                if len(palabra) > 3 and not palabra.isdigit() and '€' not in palabra:
                    vino_data['bodega'] = palabra
                    break
        
        return vino_data
    
    def scraping_completo_vivino(self, url=None, max_vinos=50):
        """Realiza scraping completo de Vivino con estrategias múltiples"""
        
        if not url:
            # URL optimizada para vinos españoles
            url = "https://www.vivino.com/explore?e=eJwFwUsKgCAUBdDd3GFEQp_BHbaBoFFEmBpIWtLru_vOsYmLDuIQD6qsRvQbK0T9ssxh2PYdEhVuQ-yHpXVisM8fZyfnlLxZBQ-3KwQ8Moxsih82Qhr5"
        
        print(f"🚀 Iniciando scraping avanzado de Vivino")
        print(f"🌐 URL objetivo: {url}")
        print(f"📊 Máximo de vinos: {max_vinos}")
        print(f"🔑 Session ID: {self.session_id}")
        
        try:
            # Navegar a la página
            self.driver.get(url)
            print("⏳ Cargando página inicial...")
            time.sleep(5 + random.uniform(1, 3))
            
            # Scroll inteligente
            self.scroll_inteligente(pausas=4)
            
            # Obtener HTML
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            
            print("🔍 Analizando contenido de la página...")
            
            # Estrategias múltiples para encontrar vinos
            estrategias = [
                # Estrategia 1: Enlaces con '/w/' (vinos)
                lambda: soup.find_all('a', href=lambda x: x and '/w/' in str(x)),
                # Estrategia 2: Elementos con clases específicas de vinos
                lambda: soup.find_all(['div', 'article'], class_=lambda x: x and any(term in str(x).lower() for term in ['wine', 'product', 'card'])),
                # Estrategia 3: Enlaces que contienen texto de precio
                lambda: soup.find_all('a', string=lambda x: x and '€' in str(x))
            ]
            
            vinos_encontrados = set()
            
            for i, estrategia in enumerate(estrategias, 1):
                print(f"   Ejecutando estrategia {i}...")
                elementos = estrategia()
                print(f"   Encontrados {len(elementos)} elementos")
                
                for elemento in elementos:
                    if len(vinos_encontrados) >= max_vinos:
                        break
                    
                    # Extraer información del elemento
                    texto = elemento.get_text(strip=True) if hasattr(elemento, 'get_text') else str(elemento)
                    href = elemento.get('href') if elemento.name == 'a' else None
                    
                    # Filtros de calidad
                    if not texto or len(texto) < 10:
                        continue
                    
                    if '€' not in texto and not href:
                        continue
                    
                    # Crear URL completa
                    if href:
                        if href.startswith('http'):
                            url_completa = href
                        else:
                            url_completa = f"https://www.vivino.com{href}"
                    else:
                        url_completa = url
                    
                    # Evitar duplicados
                    identificador = f"{texto[:50]}_{url_completa}"
                    if identificador in vinos_encontrados:
                        continue
                    
                    vinos_encontrados.add(identificador)
                    
                    # Extraer datos del vino
                    vino_data = self.extraer_datos_vino(texto, url_completa, len(self.datos_extraidos) + 1)
                    self.datos_extraidos.append(vino_data)
            
            print(f"✅ Scraping completado: {len(self.datos_extraidos)} vinos únicos encontrados")
            
            return True
            
        except Exception as e:
            print(f"❌ Error durante el scraping: {e}")
            return False
    
    def guardar_csv_avanzado(self):
        """Guarda los datos en CSV con formato avanzado"""
        try:
            carpeta = self.crear_carpeta_datos()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Archivo individual de la sesión
            nombre_archivo = f"{carpeta}/vivino_scraping_avanzado_{timestamp}.csv"
            
            # Headers expandidos
            headers = [
                'timestamp', 'session_id', 'posicion', 'nombre_completo', 'url',
                'precio_eur', 'precio_original', 'descuento', 'bodega', 'region',
                'año', 'rating', 'num_reviews', 'categoria_calidad', 'tipo_vino',
                'disponibilidad'
            ]
            
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                
                for vino in self.datos_extraidos:
                    writer.writerow(vino)
            
            print(f"✅ CSV individual guardado: {nombre_archivo}")
            
            # Actualizar archivo histórico
            archivo_historico = f"{carpeta}/vivino_historico_avanzado.csv"
            archivo_existe = os.path.exists(archivo_historico)
            
            with open(archivo_historico, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                
                if not archivo_existe:
                    writer.writeheader()
                
                for vino in self.datos_extraidos:
                    writer.writerow(vino)
            
            print(f"✅ CSV histórico actualizado: {archivo_historico}")
            
            return nombre_archivo, archivo_historico
            
        except Exception as e:
            print(f"❌ Error guardando CSV: {e}")
            return None, None
    
    def generar_reporte(self):
        """Genera un reporte detallado del scraping"""
        if not self.datos_extraidos:
            print("⚠️ No hay datos para generar reporte")
            return
        
        # Estadísticas básicas
        total_vinos = len(self.datos_extraidos)
        vinos_con_precio = len([v for v in self.datos_extraidos if v['precio_eur']])
        vinos_con_rating = len([v for v in self.datos_extraidos if v['rating']])
        vinos_con_descuento = len([v for v in self.datos_extraidos if v['descuento']])
        
        # Precios
        precios = [v['precio_eur'] for v in self.datos_extraidos if v['precio_eur']]
        precio_min = min(precios) if precios else 0
        precio_max = max(precios) if precios else 0
        precio_promedio = sum(precios) / len(precios) if precios else 0
        
        # Ratings
        ratings = [v['rating'] for v in self.datos_extraidos if v['rating']]
        rating_promedio = sum(ratings) / len(ratings) if ratings else 0
        
        # Regiones más frecuentes
        regiones = [v['region'] for v in self.datos_extraidos if v['region']]
        regiones_frecuentes = {}
        for region in regiones:
            regiones_frecuentes[region] = regiones_frecuentes.get(region, 0) + 1
        
        # Imprimir reporte
        print("\n" + "="*70)
        print("📊 REPORTE DETALLADO DE SCRAPING AVANZADO - VIVINO")
        print("="*70)
        print(f"🕐 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔑 Session ID: {self.session_id}")
        print(f"🍷 Total de vinos extraídos: {total_vinos}")
        print(f"💰 Vinos con precio: {vinos_con_precio} ({vinos_con_precio/total_vinos*100:.1f}%)")
        print(f"⭐ Vinos con rating: {vinos_con_rating} ({vinos_con_rating/total_vinos*100:.1f}%)")
        print(f"🏷️ Vinos con descuento: {vinos_con_descuento}")
        
        if precios:
            print(f"\n💶 ANÁLISIS DE PRECIOS:")
            print(f"   Precio mínimo: €{precio_min:.2f}")
            print(f"   Precio máximo: €{precio_max:.2f}")
            print(f"   Precio promedio: €{precio_promedio:.2f}")
        
        if ratings:
            print(f"\n⭐ ANÁLISIS DE RATINGS:")
            print(f"   Rating promedio: {rating_promedio:.2f}")
            print(f"   Rating más alto: {max(ratings):.2f}")
            print(f"   Rating más bajo: {min(ratings):.2f}")
        
        if regiones_frecuentes:
            print(f"\n🌍 REGIONES MÁS FRECUENTES:")
            for region, count in sorted(regiones_frecuentes.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"   {region}: {count} vinos")
        
        # Top 10 vinos
        print(f"\n🏆 TOP 10 VINOS ENCONTRADOS:")
        for i, vino in enumerate(self.datos_extraidos[:10], 1):
            precio_str = f" - €{vino['precio_eur']:.2f}" if vino['precio_eur'] else ""
            rating_str = f" (⭐{vino['rating']:.1f})" if vino['rating'] else ""
            descuento_str = f" [-{vino['descuento']:.0f}%]" if vino['descuento'] else ""
            año_str = f" {vino['año']}" if vino['año'] else ""
            
            print(f"{i:2d}. {vino['bodega']}{año_str}{precio_str}{descuento_str}{rating_str}")
            if vino['region']:
                print(f"     📍 {vino['region']} - {vino['categoria_calidad']}")
        
        print("="*70)
    
    def ejecutar_scraping_completo(self, url=None, max_vinos=50):
        """Ejecuta el proceso completo de scraping"""
        print("🚀 INICIANDO SCRAPING AVANZADO DE VIVINO")
        
        if not self.configurar_driver():
            return False
        
        try:
            # Realizar scraping
            if not self.scraping_completo_vivino(url, max_vinos):
                return False
            
            # Guardar datos
            archivo_individual, archivo_historico = self.guardar_csv_avanzado()
            
            # Generar reporte
            self.generar_reporte()
            
            print("\n✅ SCRAPING AVANZADO COMPLETADO EXITOSAMENTE")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en proceso completo: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                print("🔚 Driver cerrado")


def main():
    """Función principal para ejecutar el scraper"""
    print("🍷 VIVINO SCRAPER AVANZADO - ÚLTIMA VERSIÓN")
    print("=" * 50)
    
    # Configuración
    headless = True  # Cambiar a False para ver el navegador
    max_vinos = 30   # Número máximo de vinos a extraer
    
    # URL específica (opcional)
    url_custom = None  # Usar None para URL por defecto
    
    # Crear instancia del scraper
    scraper = VivinoScraperAvanzado(headless=headless)
    
    # Ejecutar scraping
    exito = scraper.ejecutar_scraping_completo(url_custom, max_vinos)
    
    if exito:
        print("\n🎉 PROCESO COMPLETADO EXITOSAMENTE")
        print("📁 Revisa la carpeta 'datos_scraping' para los archivos CSV generados")
    else:
        print("\n❌ PROCESO FALLÓ")
        print("🔧 Revisa los errores anteriores para diagnosticar el problema")
    
    return exito


if __name__ == "__main__":
    main()
