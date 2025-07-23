#!/usr/bin/env python3
"""
Vivino Scraper Multi-Página - Extracción Completa
Script para scraping paginado de Vivino extrayendo vinos de múltiples páginas
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

class VivinoScraperMultiPagina:
    """Scraper paginado para extraer vinos de múltiples páginas de Vivino"""
    
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.datos_extraidos = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pagina_actual = 1
        self.total_paginas = 0
        
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
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            # User agents rotativos
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
    
    def scroll_suave(self):
        """Realiza scroll suave para cargar contenido dinámico"""
        print("📜 Scroll suave para cargar contenido...")
        
        # Scroll gradual hacia abajo
        for i in range(0, 3):
            scroll_position = (i + 1) * 800
            self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(1 + random.uniform(0.3, 0.8))
        
        # Scroll al final
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Scroll hacia arriba un poco
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.8);")
        time.sleep(1)
    
    def extraer_datos_vino_mejorado(self, elemento_texto, url_vino, posicion_global):
        """Extrae datos detallados de un vino con parsing mejorado"""
        
        vino_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'session_id': self.session_id,
            'pagina': self.pagina_actual,
            'posicion_pagina': posicion_global,
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
            'tipo_vino': 'Tinto',  # Por defecto, ya que la mayoría son tintos
            'descuento': None,
            'precio_original': None,
            'disponibilidad': 'Disponible'
        }
        
        # Limpiar texto para mejor parsing
        texto_limpio = re.sub(r'\s+', ' ', elemento_texto).strip()
        
        # Extraer precio actual con patrones múltiples
        patrones_precio = [
            r'(\d+[,.]?\d*)\s*€',
            r'€\s*(\d+[,.]?\d*)',
            r'(\d+[,.]?\d*)\s*euros?'
        ]
        
        for patron in patrones_precio:
            precio_match = re.search(patron, texto_limpio)
            if precio_match:
                try:
                    precio = float(precio_match.group(1).replace(',', '.'))
                    if 5 <= precio <= 500:  # Rango válido de precios
                        vino_data['precio_eur'] = precio
                        break
                except:
                    continue
        
        # Extraer rating y reviews con patrones mejorados
        patrones_rating = [
            r'(\d+[,.]?\d+)\s*(\d+)\s*valoraciones',
            r'Rating:\s*(\d+[,.]?\d+)',
            r'⭐\s*(\d+[,.]?\d+)',
            r'(\d+[,.]?\d+)\s*stars'
        ]
        
        for patron in patrones_rating:
            rating_match = re.search(patron, texto_limpio)
            if rating_match:
                try:
                    rating = float(rating_match.group(1).replace(',', '.'))
                    if 3.0 <= rating <= 5.0:  # Rango válido de ratings
                        vino_data['rating'] = rating
                        # Intentar extraer número de reviews si está en el mismo patrón
                        if len(rating_match.groups()) > 1:
                            try:
                                num_reviews = int(rating_match.group(2))
                                vino_data['num_reviews'] = num_reviews
                            except:
                                pass
                        break
                except:
                    continue
        
        # Extraer número de reviews por separado si no se obtuvo antes
        if not vino_data['num_reviews']:
            patrones_reviews = [
                r'(\d+)\s*valoraciones',
                r'(\d+)\s*reviews',
                r'(\d+)\s*ratings'
            ]
            
            for patron in patrones_reviews:
                reviews_match = re.search(patron, texto_limpio)
                if reviews_match:
                    try:
                        num_reviews = int(reviews_match.group(1))
                        if num_reviews > 0:
                            vino_data['num_reviews'] = num_reviews
                            break
                    except:
                        continue
        
        # Extraer año con validación
        año_match = re.search(r'(20\d{2}|19\d{2})', texto_limpio)
        if año_match:
            año = int(año_match.group(1))
            if 1990 <= año <= 2025:  # Rango válido de años
                vino_data['año'] = año
        
        # Extraer región con lista expandida y específica
        regiones_españa = [
            'Rioja', 'Ribera del Duero', 'Catalunya', 'Cataluña', 'Madrid',
            'Aragón', 'Castilla y León', 'Castilla', 'Extremadura', 
            'Campo de Borja', 'Calatayud', 'Terra Alta', 'Somontano',
            'Empordà', 'Cariñena', 'Valdejalón', 'Jumilla', 'Yecla',
            'Bullas', 'Almansa', 'Manchuela', 'La Mancha', 'Valdepeñas',
            'Montilla-Moriles', 'Jerez', 'Málaga', 'Galicia', 'Rías Baixas',
            'Ribeiro', 'Valdeorras', 'Monterrei', 'Navarra', 'Penedès',
            'Priorat', 'Montsant', 'Costers del Segre', 'España'
        ]
        
        for region in regiones_españa:
            if region in texto_limpio:
                vino_data['region'] = region
                break
        
        # Extraer categoría de calidad
        calidades = [
            'Great Value', 'Good Value', 'Amazing Value', 'Best Value',
            'Cosecha más antigua', 'Top Rated', 'Critics Choice',
            'Premium', 'Limited Edition', 'Organic', 'Biodynamic'
        ]
        
        for calidad in calidades:
            if calidad in texto_limpio:
                vino_data['categoria_calidad'] = calidad
                break
        
        # Extraer bodega mejorado
        # Buscar patrones específicos de bodegas
        palabras = texto_limpio.split()
        for i, palabra in enumerate(palabras[:5]):  # Revisar primeras 5 palabras
            if (len(palabra) > 3 and 
                not palabra.isdigit() and 
                '€' not in palabra and 
                not re.search(r'^\d+[,.]?\d*$', palabra) and
                palabra not in ['Good', 'Great', 'Amazing', 'Value', 'España', 'Tinto']):
                vino_data['bodega'] = palabra.replace(',', '').strip()
                break
        
        # Si no encontró bodega, usar patrones más específicos
        if not vino_data['bodega']:
            patrones_bodega = [
                r'^([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)',
                r'Bodega\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\s+Winery'
            ]
            
            for patron in patrones_bodega:
                bodega_match = re.search(patron, texto_limpio)
                if bodega_match:
                    vino_data['bodega'] = bodega_match.group(1).strip()
                    break
        
        return vino_data
    
    def buscar_boton_siguiente(self):
        """Busca y hace clic en el botón 'Siguiente' para ir a la próxima página"""
        try:
            # Múltiples selectores para el botón siguiente
            selectores_siguiente = [
                "//a[contains(text(), 'Siguiente')]",
                "//button[contains(text(), 'Siguiente')]",
                "//a[contains(text(), 'Next')]",
                "//button[contains(text(), 'Next')]",
                "//a[@aria-label='Next']",
                "//button[@aria-label='Next']",
                "//a[contains(@class, 'next')]",
                "//button[contains(@class, 'next')]",
                f"//a[contains(text(), '{self.pagina_actual + 1}')]"
            ]
            
            wait = WebDriverWait(self.driver, 10)
            
            for selector in selectores_siguiente:
                try:
                    boton = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    if boton and boton.is_enabled():
                        # Scroll al botón
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", boton)
                        time.sleep(1)
                        
                        # Hacer clic
                        boton.click()
                        print(f"✅ Navegando a página {self.pagina_actual + 1}")
                        time.sleep(3 + random.uniform(1, 2))
                        return True
                        
                except (TimeoutException, NoSuchElementException):
                    continue
            
            print(f"⚠️ No se encontró botón 'Siguiente' en página {self.pagina_actual}")
            return False
            
        except Exception as e:
            print(f"❌ Error buscando botón siguiente: {e}")
            return False
    
    def extraer_vinos_pagina_actual(self):
        """Extrae todos los vinos de la página actual"""
        print(f"🔍 Extrayendo vinos de página {self.pagina_actual}...")
        
        # Scroll para cargar contenido
        self.scroll_suave()
        
        # Obtener HTML
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        
        vinos_pagina = []
        
        # Estrategias para encontrar vinos en la página actual
        estrategias = [
            # Enlaces de vinos con /w/
            lambda: soup.find_all('a', href=lambda x: x and '/w/' in str(x)),
            # Elementos con clases de producto/vino
            lambda: soup.find_all(['div', 'article', 'li'], class_=lambda x: x and any(
                term in str(x).lower() for term in ['wine', 'product', 'card', 'item']
            )),
            # Enlaces que contienen precios
            lambda: soup.find_all('a', string=lambda x: x and '€' in str(x))
        ]
        
        vinos_encontrados = set()
        
        for i, estrategia in enumerate(estrategias, 1):
            print(f"   Ejecutando estrategia {i} en página {self.pagina_actual}...")
            elementos = estrategia()
            print(f"   Encontrados {len(elementos)} elementos potenciales")
            
            for elemento in elementos:
                # Extraer información del elemento
                texto = elemento.get_text(strip=True) if hasattr(elemento, 'get_text') else str(elemento)
                href = elemento.get('href') if elemento.name == 'a' else None
                
                # Filtros de calidad
                if not texto or len(texto) < 15:
                    continue
                
                # Debe contener precio o ser un enlace de vino
                if '€' not in texto and not (href and '/w/' in href):
                    continue
                
                # Evitar elementos de navegación
                if any(nav_term in texto.lower() for nav_term in ['anterior', 'siguiente', 'página', 'filtros', 'ordenar']):
                    continue
                
                # Crear URL completa
                if href:
                    url_completa = href if href.startswith('http') else f"https://www.vivino.com{href}"
                else:
                    url_completa = self.driver.current_url
                
                # Evitar duplicados
                identificador = f"{texto[:80]}_{url_completa}"
                if identificador in vinos_encontrados:
                    continue
                
                vinos_encontrados.add(identificador)
                
                # Extraer datos del vino
                vino_data = self.extraer_datos_vino_mejorado(texto, url_completa, len(vinos_pagina) + 1)
                vinos_pagina.append(vino_data)
                
                # Limitar vinos por página para evitar sobrecarga
                if len(vinos_pagina) >= 24:  # Típicamente 24 vinos por página en Vivino
                    break
            
            if vinos_pagina:
                break  # Si encontró vinos, no necesita probar otras estrategias
        
        print(f"✅ Extraídos {len(vinos_pagina)} vinos de página {self.pagina_actual}")
        return vinos_pagina
    
    def scraping_multipagina(self, url_base=None, max_paginas=5):
        """Realiza scraping de múltiples páginas"""
        
        if not url_base:
            # URL para vinos españoles con filtros específicos
            url_base = "https://www.vivino.com/explore?e=eJwFwUsKgCAUBdDd3GFEQp_BHbaBoFFEmBpIWtLru_vOsYmLDuIQD6qsRvQbK0T9ssxh2PYdEhVuQ-yHpXVisM8fZyfnlLxZBQ-3KwQ8Moxsih82Qhr5"
        
        print(f"🚀 Iniciando scraping multi-página de Vivino")
        print(f"🌐 URL base: {url_base}")
        print(f"📊 Máximo de páginas: {max_paginas}")
        print(f"🔑 Session ID: {self.session_id}")
        
        try:
            # Navegar a la primera página
            self.driver.get(url_base)
            print("⏳ Cargando página inicial...")
            time.sleep(5 + random.uniform(1, 3))
            
            total_vinos_extraidos = 0
            
            for pagina in range(1, max_paginas + 1):
                self.pagina_actual = pagina
                print(f"\n📄 PROCESANDO PÁGINA {pagina}/{max_paginas}")
                
                # Extraer vinos de la página actual
                vinos_pagina = self.extraer_vinos_pagina_actual()
                
                if not vinos_pagina:
                    print(f"⚠️ No se encontraron vinos en página {pagina}. Finalizando...")
                    break
                
                # Agregar vinos extraídos
                self.datos_extraidos.extend(vinos_pagina)
                total_vinos_extraidos += len(vinos_pagina)
                
                print(f"📊 Total acumulado: {total_vinos_extraidos} vinos")
                
                # Guardar progreso cada 2 páginas
                if pagina % 2 == 0:
                    self.guardar_progreso_temporal()
                
                # Si no es la última página, navegar a la siguiente
                if pagina < max_paginas:
                    print(f"🔄 Navegando a página {pagina + 1}...")
                    
                    if not self.buscar_boton_siguiente():
                        print(f"⚠️ No se puede navegar a página {pagina + 1}. Finalizando...")
                        break
                    
                    # Pausa entre páginas
                    time.sleep(3 + random.uniform(1, 2))
            
            print(f"\n✅ Scraping multi-página completado")
            print(f"📊 Total de vinos extraídos: {len(self.datos_extraidos)}")
            print(f"📄 Páginas procesadas: {self.pagina_actual}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error durante scraping multi-página: {e}")
            return False
    
    def guardar_progreso_temporal(self):
        """Guarda progreso temporal durante el scraping"""
        try:
            carpeta = self.crear_carpeta_datos()
            archivo_temporal = f"{carpeta}/vivino_scraping_progreso_{self.session_id}.csv"
            
            headers = [
                'timestamp', 'session_id', 'pagina', 'posicion_pagina', 'posicion_global',
                'nombre_completo', 'url', 'precio_eur', 'precio_original', 'descuento',
                'bodega', 'region', 'año', 'rating', 'num_reviews', 'categoria_calidad',
                'tipo_vino', 'disponibilidad'
            ]
            
            with open(archivo_temporal, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                
                for vino in self.datos_extraidos:
                    writer.writerow(vino)
            
            print(f"💾 Progreso guardado: {archivo_temporal}")
            
        except Exception as e:
            print(f"❌ Error guardando progreso: {e}")
    
    def guardar_csv_final(self):
        """Guarda los datos finales en CSV"""
        try:
            carpeta = self.crear_carpeta_datos()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Archivo individual de la sesión
            archivo_individual = f"{carpeta}/vivino_scraping_multipagina_{timestamp}.csv"
            
            headers = [
                'timestamp', 'session_id', 'pagina', 'posicion_pagina', 'posicion_global',
                'nombre_completo', 'url', 'precio_eur', 'precio_original', 'descuento',
                'bodega', 'region', 'año', 'rating', 'num_reviews', 'categoria_calidad',
                'tipo_vino', 'disponibilidad'
            ]
            
            with open(archivo_individual, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                
                for vino in self.datos_extraidos:
                    writer.writerow(vino)
            
            print(f"✅ CSV final guardado: {archivo_individual}")
            
            # Actualizar histórico
            archivo_historico = f"{carpeta}/vivino_historico_multipagina.csv"
            archivo_existe = os.path.exists(archivo_historico)
            
            with open(archivo_historico, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                
                if not archivo_existe:
                    writer.writeheader()
                
                for vino in self.datos_extraidos:
                    writer.writerow(vino)
            
            print(f"✅ CSV histórico actualizado: {archivo_historico}")
            
            return archivo_individual, archivo_historico
            
        except Exception as e:
            print(f"❌ Error guardando CSV final: {e}")
            return None, None
    
    def generar_reporte_detallado(self):
        """Genera un reporte detallado del scraping multi-página"""
        if not self.datos_extraidos:
            print("⚠️ No hay datos para generar reporte")
            return
        
        print("\n" + "="*80)
        print("📊 REPORTE DETALLADO DE SCRAPING MULTI-PÁGINA - VIVINO")
        print("="*80)
        
        # Estadísticas generales
        total_vinos = len(self.datos_extraidos)
        paginas_procesadas = max([v.get('pagina', 1) for v in self.datos_extraidos])
        
        print(f"🕐 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔑 Session ID: {self.session_id}")
        print(f"📄 Páginas procesadas: {paginas_procesadas}")
        print(f"🍷 Total de vinos extraídos: {total_vinos}")
        print(f"📊 Promedio por página: {total_vinos/paginas_procesadas:.1f} vinos")
        
        # Análisis por página
        print(f"\n📄 ANÁLISIS POR PÁGINA:")
        for pagina in range(1, paginas_procesadas + 1):
            vinos_pagina = [v for v in self.datos_extraidos if v.get('pagina') == pagina]
            print(f"   Página {pagina}: {len(vinos_pagina)} vinos")
        
        # Estadísticas de precios
        precios = [v['precio_eur'] for v in self.datos_extraidos if v['precio_eur']]
        if precios:
            print(f"\n💶 ANÁLISIS DE PRECIOS:")
            print(f"   Vinos con precio: {len(precios)} ({len(precios)/total_vinos*100:.1f}%)")
            print(f"   Precio mínimo: €{min(precios):.2f}")
            print(f"   Precio máximo: €{max(precios):.2f}")
            print(f"   Precio promedio: €{sum(precios)/len(precios):.2f}")
        
        # Estadísticas de ratings
        ratings = [v['rating'] for v in self.datos_extraidos if v['rating']]
        if ratings:
            print(f"\n⭐ ANÁLISIS DE RATINGS:")
            print(f"   Vinos con rating: {len(ratings)} ({len(ratings)/total_vinos*100:.1f}%)")
            print(f"   Rating promedio: {sum(ratings)/len(ratings):.2f}")
            print(f"   Rating más alto: {max(ratings):.2f}")
            print(f"   Rating más bajo: {min(ratings):.2f}")
        
        # Regiones más frecuentes
        regiones = [v['region'] for v in self.datos_extraidos if v['region']]
        regiones_count = {}
        for region in regiones:
            regiones_count[region] = regiones_count.get(region, 0) + 1
        
        if regiones_count:
            print(f"\n🌍 REGIONES MÁS FRECUENTES:")
            for region, count in sorted(regiones_count.items(), key=lambda x: x[1], reverse=True)[:8]:
                print(f"   {region}: {count} vinos")
        
        # Categorías de calidad
        calidades = [v['categoria_calidad'] for v in self.datos_extraidos if v['categoria_calidad']]
        calidades_count = {}
        for calidad in calidades:
            calidades_count[calidad] = calidades_count.get(calidad, 0) + 1
        
        if calidades_count:
            print(f"\n🏆 CATEGORÍAS DE CALIDAD:")
            for calidad, count in sorted(calidades_count.items(), key=lambda x: x[1], reverse=True):
                print(f"   {calidad}: {count} vinos")
        
        # Top vinos por página
        print(f"\n🍷 TOP VINOS POR PÁGINA:")
        for pagina in range(1, min(paginas_procesadas + 1, 4)):  # Mostrar hasta 3 páginas
            vinos_pagina = [v for v in self.datos_extraidos if v.get('pagina') == pagina]
            print(f"\n   📄 PÁGINA {pagina}:")
            for i, vino in enumerate(vinos_pagina[:5], 1):  # Top 5 por página
                precio_str = f" - €{vino['precio_eur']:.2f}" if vino['precio_eur'] else ""
                rating_str = f" (⭐{vino['rating']:.1f})" if vino['rating'] else ""
                año_str = f" {vino['año']}" if vino['año'] else ""
                
                print(f"   {i}. {vino['bodega']}{año_str}{precio_str}{rating_str}")
                if vino['region']:
                    print(f"      📍 {vino['region']} - {vino['categoria_calidad']}")
        
        print("="*80)
    
    def ejecutar_scraping_completo(self, url=None, max_paginas=5):
        """Ejecuta el proceso completo de scraping multi-página"""
        print("🚀 INICIANDO SCRAPING MULTI-PÁGINA DE VIVINO")
        
        if not self.configurar_driver():
            return False
        
        try:
            # Realizar scraping multi-página
            if not self.scraping_multipagina(url, max_paginas):
                return False
            
            # Guardar datos finales
            archivo_individual, archivo_historico = self.guardar_csv_final()
            
            # Generar reporte detallado
            self.generar_reporte_detallado()
            
            print("\n✅ SCRAPING MULTI-PÁGINA COMPLETADO EXITOSAMENTE")
            print(f"📁 Archivos generados:")
            if archivo_individual:
                print(f"   - Individual: {archivo_individual}")
            if archivo_historico:
                print(f"   - Histórico: {archivo_historico}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en proceso completo: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                print("🔚 Driver cerrado")


def main():
    """Función principal para ejecutar el scraper multi-página"""
    print("🍷 VIVINO SCRAPER MULTI-PÁGINA - EXTRACCIÓN COMPLETA")
    print("=" * 60)
    
    # Configuración
    headless = True      # Cambiar a False para ver el navegador
    max_paginas = 3      # Número de páginas a procesar
    
    # URL específica (opcional)
    url_custom = None    # Usar None para URL por defecto
    
    # Crear instancia del scraper
    scraper = VivinoScraperMultiPagina(headless=headless)
    
    # Ejecutar scraping multi-página
    exito = scraper.ejecutar_scraping_completo(url_custom, max_paginas)
    
    if exito:
        print("\n🎉 PROCESO MULTI-PÁGINA COMPLETADO EXITOSAMENTE")
        print("📁 Revisa la carpeta 'datos_scraping' para los archivos CSV generados")
        print("📊 Se han extraído vinos de múltiples páginas de Vivino")
    else:
        print("\n❌ PROCESO MULTI-PÁGINA FALLÓ")
        print("🔧 Revisa los errores anteriores para diagnosticar el problema")
    
    return exito


if __name__ == "__main__":
    main()
