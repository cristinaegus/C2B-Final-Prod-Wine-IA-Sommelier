#!/usr/bin/env python3
"""
Vivino Scraper Diversificado - Múltiples Categorías y Regiones
Script que extrae vinos de diferentes categorías, regiones y filtros para mayor diversidad
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import os
import re
import json
from datetime import datetime
import random

class VivinoScraperDiversificado:
    """Scraper que extrae vinos de múltiples categorías y regiones para mayor diversidad"""
    
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.datos_extraidos = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.urls_procesadas = set()
        
    def configurar_driver(self):
        """Configura el driver de Chrome optimizado"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # Opciones de rendimiento
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-web-security')
            
            # User agent
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            chrome_options.add_argument(f'--user-agent={user_agent}')
            
            # Configuraciones anti-detección
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Desactivar notificaciones
            prefs = {
                "profile.default_content_setting_values": {
                    "notifications": 2,
                    "popups": 2,
                    "geolocation": 2,
                }
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Scripts anti-detección
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
        return carpeta
    
    def cerrar_popups(self):
        """Cierra pop-ups y elementos molestos"""
        try:
            selectores_cerrar = [
                "//button[contains(@class, 'close')]",
                "//button[contains(@aria-label, 'Close')]",
                "//button[contains(text(), '×')]",
                "//button[contains(text(), 'Cerrar')]",
                "//*[contains(@class, 'cookie')]//button",
                "//div[@role='dialog']//button"
            ]
            
            for selector in selectores_cerrar:
                try:
                    elementos = self.driver.find_elements(By.XPATH, selector)
                    for elemento in elementos:
                        if elemento.is_displayed() and elemento.is_enabled():
                            elemento.click()
                            time.sleep(0.5)
                except:
                    continue
                    
        except Exception as e:
            pass  # Ignorar errores de pop-ups
    
    def obtener_urls_diversificadas(self):
        """Genera URLs con diferentes filtros para obtener vinos diversos"""
        
        urls_base = []
        
        # URLs por regiones españolas específicas
        regiones_urls = [
            # Rioja
            "https://www.vivino.com/explore?e=eJzLLU4sSswtzmMYm%2BAf7O1tZGRkbGJiYGBgZGhhYmBgYGxhYmBgYGJpYmBgYGFpaGBgYGZmYGBgZmlkYGBgZGVgYGBgZmRoYGBgZWFmYGBgYWVoYGBgZWZgYGBgY2FgYGBgY2JkYGBgY2ZmYGBgZGNoYGBgZGFiYGBgZWJkYGBgZWZoYGBgZGVmYGBgZWNgYGBgZ2JgYGBgZ2ZmYGBgZGNkYGBgZWFmYGBgZWVkYGBgZWZgYGBgZWNmYGBgZGNhYGBgZGVlYGBgZGZhYGBgZGVgYGBgZGNoYGBgZGFmYGBgZWJkYGBgZWZoYGBgYmNmYGBgYmVhYGBgYmZlYGBgYmNhYGBgYmVlYGBgYmZhYGBgYmNgYGBgYmFmYGBgYmJkYGBgYmZoYGBgZGNmYGBgZWFhYGBgZWVlYGBgZWZhYGBgZWNhYGBgZWVhYGBgZWZlYGBgZGFhYGBgZGVlYGBgZGZhYGBgZGFmYGBgZGJkYGBgZGZoYGBgZWFhYGBgZWVlYGBgZWZhYGBgZWFmYGBgZWJkYGBgZWZoYGBgZGFgYGBgZGVlYGBgZGZhYGBgZGFiYGBgZGVmYGBgZGZiYGBgZGFkYGBgZGVkYGBgZGZkYGBgZGFmYGBgZGJmYGBgZGZmYGBgZWFiYGBgZWVmYGBgZWZiYGBgZWFkYGBgZWVkYGBgZWZkYGBgZWFmYGBgZWJmYGBgZWZmYGBgZGFkYGBgZGVmYGBgZGZkYGBgZGFgYGBgZGVhYGBgZGZhYGBgZGFhYGBgZGVhYGBgZGZhYGBgZGFmYGBgZGJmYGBgZGZmYGBgZWFkYGBgZWVmYGBgZWZkYGBgZWFgYGBgZWVhYGBgZWZhYGBgZWFhYGBgZWVhYGBgZWZhYGBgZWFmYGBgZWJmYGBgZWZmYGBgZGFgYGBgZGVhYGBgZGZhYGBgZGFhYGBgZGVhYGBgZGZhYGBgZGFmYGBgZGJmYGBgZGZmYGBgZWFgYGBgZWVhYGBgZWZhYGBgZWFhYGBgZWVhYGBgZWZhYGBgZWFmYGBgZWJmYGBgZWZmYGBgZGFgYGBgZGVhYGBgZGZhYGBgZGFhYGBgZGVhYGBgZGZhYGBgZGFmYGBgZGJmYGBgZGZmYGBgZWFgYGBgZWVhYGBgZWZhYGBgZWFhYGBgZWVhYGBgZWZhYGBgZWFmYGBgZWJmYGBgZWZmYGBgZGFgYGBgZGVhYGBgZGZhYGBgZGFhYGBgZGVhYGBgZGZhYGBgZGFmYGBgZGJmYGBgZGZmYGBgZWFgYGBgZWVhYGBgZWZhYGBgZWFhYGBgZWVhYGBgZWZhYGBgZWFmYGBgZWJmYGBgZWZmYGBgZGFgYGBgZGVhYGBgZGZhYGBgZGFhYGBgZGVhYGBgZGZhYGBgZGFmYGBgZGJmYGBgZGZmYGBgZWFgYGBgZWVhYGBgZWZhYGBgZWFhYGBgZWVhYGBgZWZhYGBgZWFmYGBgZWJmYGBgZWZmYGBgZGFgYGBgZGVhYGBgZGZhYGBgZGFhYGBgZGVhYGBgZGZhYGBgZGFmYGBgZGJmYGBgZGZmYGBgZWFgYGBgZWVhYGBgZWZhYGBgZWFhYGBgZWVhYGBgZWZhYGBgZWFmYGBgZWJmYGBgZWZmYGBgZGFgYGBgZGVhYGBgZGZhYGBgZGFhYGBgZGVhYGBgZGZhYGBgZGFmYGBgZGJmYGBgZGZmYGBgZWFgYGBgZWVhYGBgZWZhYGBgZWFhYGBgZWVhYGBgZWZhYGBgZWFmYGBgZWJmYGBgZWZmYGBgZGFgYGBgZGVhYGBgZGZhYGBgZGFhYGBgZGVhYGBgZGZhYGBgZGFmYGBgZGJmYGBgZGZmYGBgZWFgYGBgZWVhYGBgZWZhYGBgZWFhYGBgZWVhYGBgZWZhYGBgZWFmYGBgZWJmYGBgZWZmYGBgZGFgYGBgZGVhYGBgZGZhYGBgZGFhYGBgZGVhYGBgZGZhYGBgZGFmYGBgZGJmYGBgZGZmYGBgZWFgYGBgZWVhYGBgZWZhYGBgZWFhYGBgZWVhYGBgZWZhYGBgZWFmYGBgZWJmYGBgZWZmYGBg&wine_style_ids[]=92",
            
            # Ribera del Duero
            "https://www.vivino.com/explore?country_codes[]=es&region_codes[]=59&wine_style_ids[]=92",
            
            # Catalunya/Cataluña
            "https://www.vivino.com/explore?country_codes[]=es&region_codes[]=52&wine_style_ids[]=92",
            
            # Madrid
            "https://www.vivino.com/explore?country_codes[]=es&region_codes[]=61&wine_style_ids[]=92",
            
            # Navarra
            "https://www.vivino.com/explore?country_codes[]=es&region_codes[]=62&wine_style_ids[]=92"
        ]
        
        # URLs con diferentes rangos de precio
        precios_urls = [
            # Vinos baratos (€5-€15)
            "https://www.vivino.com/explore?country_codes[]=es&price_range_min=5&price_range_max=15&wine_style_ids[]=92",
            
            # Vinos medios (€15-€30)
            "https://www.vivino.com/explore?country_codes[]=es&price_range_min=15&price_range_max=30&wine_style_ids[]=92",
            
            # Vinos premium (€30-€60)
            "https://www.vivino.com/explore?country_codes[]=es&price_range_min=30&price_range_max=60&wine_style_ids[]=92",
            
            # Vinos de lujo (€60+)
            "https://www.vivino.com/explore?country_codes[]=es&price_range_min=60&wine_style_ids[]=92"
        ]
        
        # URLs con diferentes ordenamientos
        ordenamiento_urls = [
            # Más populares
            "https://www.vivino.com/explore?country_codes[]=es&order_by=most_popular&wine_style_ids[]=92",
            
            # Mejor valorados
            "https://www.vivino.com/explore?country_codes[]=es&order_by=highest_rated&min_rating=4.0&wine_style_ids[]=92",
            
            # Más baratos
            "https://www.vivino.com/explore?country_codes[]=es&order_by=price&order=asc&wine_style_ids[]=92",
            
            # Más caros
            "https://www.vivino.com/explore?country_codes[]=es&order_by=price&order=desc&wine_style_ids[]=92"
        ]
        
        # URLs con diferentes años
        años_urls = [
            # Vinos recientes (2020-2023)
            "https://www.vivino.com/explore?country_codes[]=es&year_min=2020&year_max=2023&wine_style_ids[]=92",
            
            # Vinos maduros (2015-2019)
            "https://www.vivino.com/explore?country_codes[]=es&year_min=2015&year_max=2019&wine_style_ids[]=92",
            
            # Vinos añejos (2010-2014)
            "https://www.vivino.com/explore?country_codes[]=es&year_min=2010&year_max=2014&wine_style_ids[]=92"
        ]
        
        # Combinar todas las URLs
        urls_base.extend(regiones_urls[:3])  # Primeras 3 regiones
        urls_base.extend(precios_urls[:3])   # Primeros 3 rangos de precio
        urls_base.extend(ordenamiento_urls[:2])  # Primeros 2 ordenamientos
        urls_base.extend(años_urls[:2])      # Primeros 2 rangos de años
        
        return urls_base
    
    def extraer_datos_vino_completo(self, elemento_texto, url_vino, categoria, posicion):
        """Extrae datos completos de un vino"""
        
        vino_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'session_id': self.session_id,
            'categoria_busqueda': categoria,
            'posicion': posicion,
            'posicion_global': len(self.datos_extraidos) + 1,
            'nombre_completo': elemento_texto,
            'url': url_vino,
            'precio_eur': None,
            'bodega': '',
            'region': '',
            'año': None,
            'rating': None,
            'num_reviews': None,
            'categoria_calidad': '',
            'tipo_vino': 'Tinto',
            'descuento': None,
            'precio_original': None,
            'disponibilidad': 'Disponible'
        }
        
        # Limpiar texto
        texto = re.sub(r'\s+', ' ', elemento_texto).strip()
        
        # Extraer precio
        patrones_precio = [
            r'(\d+[,.]?\d*)\s*€',
            r'€\s*(\d+[,.]?\d*)',
            r'Price:\s*€?(\d+[,.]?\d*)'
        ]
        
        for patron in patrones_precio:
            match = re.search(patron, texto)
            if match:
                try:
                    precio = float(match.group(1).replace(',', '.'))
                    if 3 <= precio <= 1000:  # Rango muy amplio
                        vino_data['precio_eur'] = precio
                        break
                except:
                    continue
        
        # Extraer rating y reviews
        patrones_rating = [
            r'(\d+[,.]?\d+)\s*(\d+[,.]?\d*)\s*valoraciones',
            r'Rating:\s*(\d+[,.]?\d+)',
            r'(\d+[,.]?\d+)\s*★'
        ]
        
        for patron in patrones_rating:
            match = re.search(patron, texto)
            if match:
                try:
                    rating = float(match.group(1).replace(',', '.'))
                    if 1.0 <= rating <= 5.0:
                        vino_data['rating'] = rating
                        
                        # Extraer reviews si están disponibles
                        if len(match.groups()) > 1 and match.group(2):
                            try:
                                reviews = int(float(match.group(2).replace(',', '')))
                                if reviews > 0:
                                    vino_data['num_reviews'] = reviews
                            except:
                                pass
                        break
                except:
                    continue
        
        # Extraer año
        año_match = re.search(r'(20\d{2}|19\d{2})', texto)
        if año_match:
            año = int(año_match.group(1))
            if 1985 <= año <= 2025:
                vino_data['año'] = año
        
        # Extraer región
        regiones_esp = [
            'Rioja', 'Ribera del Duero', 'Catalunya', 'Cataluña', 'Madrid',
            'Aragón', 'Castilla y León', 'Campo de Borja', 'Calatayud',
            'Terra Alta', 'Somontano', 'Empordà', 'Cariñena', 'Valdejalón',
            'Navarra', 'Penedès', 'Priorat', 'Montsant', 'Costers del Segre',
            'Jumilla', 'Yecla', 'Bullas', 'La Mancha', 'Valdepeñas',
            'Montilla-Moriles', 'Jerez', 'Rías Baixas', 'Ribeiro',
            'Valdeorras', 'Bierzo', 'Toro', 'Rueda', 'España'
        ]
        
        for region in regiones_esp:
            if region in texto:
                vino_data['region'] = region
                break
        
        # Extraer categoría de calidad
        calidades = [
            'Great Value', 'Good Value', 'Amazing Value', 'Best Value',
            'Excellent Value', 'Outstanding Value', 'Top Rated',
            'Critics Choice', 'Premium', 'Limited Edition', 'Organic',
            'Cosecha más antigua', 'Vintage', 'Reserve', 'Crianza',
            'Reserva', 'Gran Reserva'
        ]
        
        for calidad in calidades:
            if calidad in texto:
                vino_data['categoria_calidad'] = calidad
                break
        
        # Extraer bodega (mejorado)
        palabras = texto.split()
        for i, palabra in enumerate(palabras[:8]):
            if (len(palabra) > 2 and 
                not palabra.isdigit() and 
                '€' not in palabra and 
                not re.match(r'^\d+[,.]?\d*$', palabra) and
                palabra.lower() not in ['good', 'great', 'amazing', 'value', 'españa', 'tinto', 'red', 'wine', 'vintage']):
                
                # Intentar capturar nombre completo de bodega
                if i < len(palabras) - 1 and len(palabras[i+1]) > 2:
                    bodega_candidata = f"{palabra} {palabras[i+1]}"
                    if len(bodega_candidata) <= 30:  # Evitar nombres muy largos
                        vino_data['bodega'] = bodega_candidata
                    else:
                        vino_data['bodega'] = palabra
                else:
                    vino_data['bodega'] = palabra
                break
        
        return vino_data
    
    def extraer_vinos_url(self, url, categoria, max_vinos=15):
        """Extrae vinos de una URL específica"""
        print(f"🔍 Extrayendo de: {categoria}")
        
        try:
            self.driver.get(url)
            time.sleep(3 + random.uniform(1, 2))
            
            # Cerrar pop-ups
            self.cerrar_popups()
            
            # Scroll gradual
            for i in range(3):
                scroll_pos = (i + 1) * 800
                self.driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
                time.sleep(1)
            
            # Obtener HTML
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Buscar enlaces de vinos
            enlaces_vino = soup.find_all('a', href=lambda x: x and '/w/' in str(x))
            
            vinos_categoria = []
            urls_vistas = set()
            
            for enlace in enlaces_vino:
                try:
                    href = enlace.get('href')
                    if not href:
                        continue
                    
                    # URL completa
                    url_completa = href if href.startswith('http') else f"https://www.vivino.com{href}"
                    
                    # Evitar duplicados globales y locales
                    if url_completa in self.urls_procesadas or url_completa in urls_vistas:
                        continue
                    
                    urls_vistas.add(url_completa)
                    self.urls_procesadas.add(url_completa)
                    
                    # Obtener texto del contenedor
                    contenedor = enlace.find_parent(['div', 'article', 'li', 'section'])
                    if contenedor:
                        texto_completo = contenedor.get_text(strip=True)
                    else:
                        texto_completo = enlace.get_text(strip=True)
                    
                    # Filtros básicos
                    if len(texto_completo) < 15:
                        continue
                    
                    if not ('€' in texto_completo or 'price' in texto_completo.lower()):
                        continue
                    
                    # Extraer datos
                    vino_data = self.extraer_datos_vino_completo(
                        texto_completo, 
                        url_completa, 
                        categoria, 
                        len(vinos_categoria) + 1
                    )
                    
                    vinos_categoria.append(vino_data)
                    
                    # Limitar vinos por categoría
                    if len(vinos_categoria) >= max_vinos:
                        break
                        
                except Exception as e:
                    continue
            
            print(f"   ✅ Extraídos {len(vinos_categoria)} vinos de {categoria}")
            return vinos_categoria
            
        except Exception as e:
            print(f"   ❌ Error en {categoria}: {e}")
            return []
    
    def scraping_diversificado(self, max_vinos_por_categoria=12):
        """Realiza scraping diversificado por categorías"""
        print("🚀 Iniciando scraping diversificado de Vivino")
        
        urls_diversas = self.obtener_urls_diversificadas()
        categorias = [
            "Rioja Premium", "Ribera del Duero", "Catalunya Moderna",
            "Vinos Baratos €5-15", "Vinos Medios €15-30", "Vinos Premium €30-60",
            "Más Populares", "Mejor Valorados",
            "Vinos Recientes 2020-23", "Vinos Maduros 2015-19"
        ]
        
        total_vinos = 0
        
        for i, (url, categoria) in enumerate(zip(urls_diversas, categorias)):
            print(f"\n📂 CATEGORÍA {i+1}/{len(urls_diversas)}: {categoria}")
            
            vinos_categoria = self.extraer_vinos_url(url, categoria, max_vinos_por_categoria)
            
            if vinos_categoria:
                self.datos_extraidos.extend(vinos_categoria)
                total_vinos += len(vinos_categoria)
                print(f"📊 Total acumulado: {total_vinos} vinos únicos")
            
            # Pausa entre categorías
            if i < len(urls_diversas) - 1:
                tiempo_pausa = 2 + random.uniform(0.5, 1.5)
                print(f"⏱️ Pausa de {tiempo_pausa:.1f}s...")
                time.sleep(tiempo_pausa)
        
        print(f"\n✅ Scraping diversificado completado")
        print(f"🍷 Total de vinos únicos extraídos: {len(self.datos_extraidos)}")
        print(f"📂 Categorías procesadas: {len(categorias)}")
        
        return len(self.datos_extraidos) > 0
    
    def guardar_csv_diversificado(self):
        """Guarda los datos diversificados en CSV"""
        try:
            carpeta = self.crear_carpeta_datos()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            headers = [
                'timestamp', 'session_id', 'categoria_busqueda', 'posicion', 'posicion_global',
                'nombre_completo', 'url', 'precio_eur', 'precio_original', 'descuento',
                'bodega', 'region', 'año', 'rating', 'num_reviews', 'categoria_calidad',
                'tipo_vino', 'disponibilidad'
            ]
            
            # Archivo individual
            archivo_individual = f"{carpeta}/vivino_diversificado_{timestamp}.csv"
            with open(archivo_individual, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                for vino in self.datos_extraidos:
                    writer.writerow(vino)
            
            print(f"✅ CSV diversificado guardado: {archivo_individual}")
            
            # Histórico
            archivo_historico = f"{carpeta}/vivino_historico_diversificado.csv"
            archivo_existe = os.path.exists(archivo_historico)
            
            with open(archivo_historico, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                if not archivo_existe:
                    writer.writeheader()
                for vino in self.datos_extraidos:
                    writer.writerow(vino)
            
            print(f"✅ CSV histórico diversificado actualizado: {archivo_historico}")
            
            return archivo_individual, archivo_historico
            
        except Exception as e:
            print(f"❌ Error guardando CSV: {e}")
            return None, None
    
    def generar_reporte_diversificado(self):
        """Genera reporte del scraping diversificado"""
        if not self.datos_extraidos:
            print("⚠️ No hay datos para generar reporte")
            return
        
        print("\n" + "="*80)
        print("📊 REPORTE DIVERSIFICADO - VIVINO MULTI-CATEGORÍA")
        print("="*80)
        
        total_vinos = len(self.datos_extraidos)
        
        print(f"🕐 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔑 Session ID: {self.session_id}")
        print(f"🍷 Total de vinos únicos: {total_vinos}")
        
        # Análisis por categoría
        categorias = {}
        for v in self.datos_extraidos:
            cat = v.get('categoria_busqueda', 'Sin categoría')
            categorias[cat] = categorias.get(cat, 0) + 1
        
        if categorias:
            print(f"\n📂 DISTRIBUCIÓN POR CATEGORÍA:")
            for cat, count in sorted(categorias.items(), key=lambda x: x[1], reverse=True):
                print(f"   {cat}: {count} vinos")
        
        # Análisis de precios
        precios = [v['precio_eur'] for v in self.datos_extraidos if v['precio_eur']]
        if precios:
            print(f"\n💶 ANÁLISIS DE PRECIOS:")
            print(f"   Vinos con precio: {len(precios)} ({len(precios)/total_vinos*100:.1f}%)")
            print(f"   Rango: €{min(precios):.2f} - €{max(precios):.2f}")
            print(f"   Promedio: €{sum(precios)/len(precios):.2f}")
            print(f"   Mediana: €{sorted(precios)[len(precios)//2]:.2f}")
        
        # Análisis de ratings
        ratings = [v['rating'] for v in self.datos_extraidos if v['rating']]
        if ratings:
            print(f"\n⭐ ANÁLISIS DE RATINGS:")
            print(f"   Vinos con rating: {len(ratings)} ({len(ratings)/total_vinos*100:.1f}%)")
            print(f"   Rating promedio: {sum(ratings)/len(ratings):.2f}")
            print(f"   Rango: {min(ratings):.1f} - {max(ratings):.1f}")
        
        # Top regiones
        regiones = {}
        for v in self.datos_extraidos:
            if v['region']:
                regiones[v['region']] = regiones.get(v['region'], 0) + 1
        
        if regiones:
            print(f"\n🌍 TOP REGIONES DIVERSIFICADAS:")
            for region, count in sorted(regiones.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"   {region}: {count} vinos")
        
        # Análisis de años
        años = [v['año'] for v in self.datos_extraidos if v['año']]
        if años:
            años_count = {}
            for año in años:
                años_count[año] = años_count.get(año, 0) + 1
            
            print(f"\n📅 TOP AÑOS:")
            for año, count in sorted(años_count.items(), key=lambda x: x[1], reverse=True)[:8]:
                print(f"   {año}: {count} vinos")
        
        print("="*80)
    
    def ejecutar_scraping_diversificado_completo(self, max_vinos_por_categoria=12):
        """Ejecuta el proceso completo de scraping diversificado"""
        print("🚀 INICIANDO SCRAPING DIVERSIFICADO DE VIVINO")
        
        if not self.configurar_driver():
            return False
        
        try:
            # Realizar scraping diversificado
            if not self.scraping_diversificado(max_vinos_por_categoria):
                return False
            
            # Guardar datos
            self.guardar_csv_diversificado()
            
            # Generar reporte
            self.generar_reporte_diversificado()
            
            print("\n✅ SCRAPING DIVERSIFICADO COMPLETADO EXITOSAMENTE")
            return True
            
        except Exception as e:
            print(f"❌ Error en proceso diversificado: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                print("🔚 Driver cerrado")


def main():
    """Función principal para scraping diversificado"""
    print("🍷 VIVINO SCRAPER DIVERSIFICADO - MÚLTIPLES CATEGORÍAS")
    print("=" * 60)
    
    # Configuración
    headless = True                    # Cambiar a False para ver navegador
    max_vinos_por_categoria = 10       # Vinos por categoría
    
    # Crear y ejecutar scraper
    scraper = VivinoScraperDiversificado(headless=headless)
    exito = scraper.ejecutar_scraping_diversificado_completo(max_vinos_por_categoria)
    
    if exito:
        print("\n🎉 PROCESO DIVERSIFICADO COMPLETADO CON ÉXITO")
        print("📁 Se han extraído vinos de múltiples categorías, regiones y filtros")
        print("📊 Revisa la carpeta 'datos_scraping' para los archivos CSV")
    else:
        print("\n❌ PROCESO DIVERSIFICADO FALLÓ")
        print("🔧 Revisa los errores anteriores")
    
    return exito


if __name__ == "__main__":
    main()
