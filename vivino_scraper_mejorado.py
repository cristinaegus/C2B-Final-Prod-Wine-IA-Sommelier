#!/usr/bin/env python3
"""
Vivino Scraper Multi-Página MEJORADO - Navegación Robusta
Script mejorado para scraping paginado de Vivino con navegación más robusta
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import os
import re
import json
from datetime import datetime
import random

class VivinoScraperMejorado:
    """Scraper mejorado con navegación robusta entre páginas"""
    
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.datos_extraidos = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pagina_actual = 1
        
    def configurar_driver(self):
        """Configura el driver de Chrome con opciones mejoradas"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # Opciones anti-detección mejoradas
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')  # Cargar más rápido
            chrome_options.add_argument('--disable-javascript')  # Evitar pop-ups
            
            # User agent más reciente
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            chrome_options.add_argument(f'--user-agent={user_agent}')
            
            # Configuraciones adicionales
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Desactivar notificaciones y pop-ups
            prefs = {
                "profile.default_content_setting_values": {
                    "notifications": 2,
                    "popups": 2,
                    "geolocation": 2,
                    "media_stream": 2,
                }
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Scripts anti-detección
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            self.driver = driver
            print("✅ Driver mejorado configurado exitosamente")
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
        """Cierra pop-ups y elementos que puedan interferir"""
        try:
            # Lista de selectores comunes de pop-ups y overlays
            selectores_cerrar = [
                "//button[contains(@class, 'close')]",
                "//button[contains(@aria-label, 'Close')]",
                "//div[contains(@class, 'modal')]//button",
                "//div[contains(@class, 'popup')]//button",
                "//div[contains(@class, 'overlay')]//button",
                "//button[contains(text(), '×')]",
                "//button[contains(text(), 'Cerrar')]",
                "//button[contains(text(), 'Close')]",
                "//div[@role='dialog']//button",
                "//*[contains(@class, 'cookie')]//button[contains(text(), 'Accept')]",
                "//*[contains(@class, 'cookie')]//button[contains(text(), 'Aceptar')]"
            ]
            
            for selector in selectores_cerrar:
                try:
                    elementos = self.driver.find_elements(By.XPATH, selector)
                    for elemento in elementos:
                        if elemento.is_displayed() and elemento.is_enabled():
                            elemento.click()
                            print("✅ Pop-up cerrado")
                            time.sleep(1)
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error cerrando pop-ups: {e}")
    
    def construir_url_pagina(self, base_url, numero_pagina):
        """Construye URL para una página específica"""
        try:
            # Si la URL ya tiene parámetros, agregar página
            if '?' in base_url:
                if 'page=' in base_url:
                    # Reemplazar el número de página existente
                    url_nueva = re.sub(r'page=\d+', f'page={numero_pagina}', base_url)
                else:
                    # Agregar parámetro de página
                    url_nueva = f"{base_url}&page={numero_pagina}"
            else:
                # URL base sin parámetros
                url_nueva = f"{base_url}?page={numero_pagina}"
            
            return url_nueva
            
        except Exception as e:
            print(f"❌ Error construyendo URL: {e}")
            return base_url
    
    def navegar_a_pagina(self, url_base, numero_pagina):
        """Navega directamente a una página específica usando URL"""
        try:
            url_pagina = self.construir_url_pagina(url_base, numero_pagina)
            print(f"🔗 Navegando a: {url_pagina}")
            
            self.driver.get(url_pagina)
            time.sleep(3 + random.uniform(1, 2))
            
            # Cerrar posibles pop-ups
            self.cerrar_popups()
            
            # Verificar que la página se cargó correctamente
            try:
                # Esperar a que aparezcan elementos de vino
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/w/')]"))
                )
                print(f"✅ Página {numero_pagina} cargada correctamente")
                return True
                
            except TimeoutException:
                print(f"⚠️ Timeout esperando contenido en página {numero_pagina}")
                return False
                
        except Exception as e:
            print(f"❌ Error navegando a página {numero_pagina}: {e}")
            return False
    
    def scroll_inteligente(self):
        """Realiza scroll inteligente para cargar todo el contenido"""
        try:
            print("📜 Realizando scroll inteligente...")
            
            # Obtener altura inicial
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            scroll_pausas = 0
            max_scrolls = 5
            
            for scroll_num in range(max_scrolls):
                # Scroll hacia abajo gradualmente
                scroll_position = (scroll_num + 1) * 600
                self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(1.5)
                
                # Verificar si el contenido cambió
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height != last_height:
                    print(f"   📄 Nuevo contenido detectado en scroll {scroll_num + 1}")
                    last_height = new_height
                    scroll_pausas = 0
                else:
                    scroll_pausas += 1
                
                # Si no hay cambios por 2 scrolls, es suficiente
                if scroll_pausas >= 2:
                    break
            
            # Scroll final al fondo
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            print("✅ Scroll inteligente completado")
            
        except Exception as e:
            print(f"❌ Error en scroll inteligente: {e}")
    
    def extraer_datos_vino_avanzado(self, elemento_texto, url_vino, posicion):
        """Extrae datos avanzados de un vino con parsing mejorado"""
        
        vino_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'session_id': self.session_id,
            'pagina': self.pagina_actual,
            'posicion_pagina': posicion,
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
        
        # Limpiar y normalizar texto
        texto = re.sub(r'\s+', ' ', elemento_texto).strip()
        
        # Extraer precio con múltiples estrategias
        patrones_precio = [
            r'(\d+[,.]?\d*)\s*€',
            r'€\s*(\d+[,.]?\d*)',
            r'Price:\s*€?(\d+[,.]?\d*)',
            r'(\d+[,.]?\d*)\s*EUR'
        ]
        
        for patron in patrones_precio:
            match = re.search(patron, texto)
            if match:
                try:
                    precio = float(match.group(1).replace(',', '.'))
                    if 5 <= precio <= 500:
                        vino_data['precio_eur'] = precio
                        break
                except:
                    continue
        
        # Extraer rating y reviews con patrones avanzados
        patrones_rating = [
            r'(\d+[,.]?\d+)\s*(\d+[,.]?\d*)\s*valoraciones',
            r'Rating:\s*(\d+[,.]?\d+)',
            r'(\d+[,.]?\d+)\s*★',
            r'⭐\s*(\d+[,.]?\d+)'
        ]
        
        for patron in patrones_rating:
            match = re.search(patron, texto)
            if match:
                try:
                    rating = float(match.group(1).replace(',', '.'))
                    if 3.0 <= rating <= 5.0:
                        vino_data['rating'] = rating
                        
                        # Intentar extraer reviews del mismo match
                        if len(match.groups()) > 1 and match.group(2):
                            try:
                                reviews = int(float(match.group(2)))
                                if reviews > 0:
                                    vino_data['num_reviews'] = reviews
                            except:
                                pass
                        break
                except:
                    continue
        
        # Extraer reviews por separado si no se obtuvo
        if not vino_data['num_reviews']:
            patrones_reviews = [
                r'(\d+[,.]?\d*)\s*valoraciones',
                r'(\d+[,.]?\d*)\s*reviews'
            ]
            for patron in patrones_reviews:
                match = re.search(patron, texto)
                if match:
                    try:
                        reviews = int(float(match.group(1).replace(',', '')))
                        if reviews > 0:
                            vino_data['num_reviews'] = reviews
                            break
                    except:
                        continue
        
        # Extraer año
        año_match = re.search(r'(20\d{2}|19\d{2})', texto)
        if año_match:
            año = int(año_match.group(1))
            if 1990 <= año <= 2025:
                vino_data['año'] = año
        
        # Extraer región (lista extendida)
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
            'Cosecha más antigua', 'Vintage'
        ]
        
        for calidad in calidades:
            if calidad in texto:
                vino_data['categoria_calidad'] = calidad
                break
        
        # Extraer bodega (primera palabra/s significativa/s)
        palabras = texto.split()
        for i, palabra in enumerate(palabras[:6]):
            if (len(palabra) > 2 and 
                not palabra.isdigit() and 
                '€' not in palabra and 
                not re.match(r'^\d+[,.]?\d*$', palabra) and
                palabra.lower() not in ['good', 'great', 'amazing', 'value', 'españa', 'tinto', 'red', 'wine']):
                
                # Tomar hasta 2 palabras para la bodega
                if i < len(palabras) - 1 and len(palabras[i+1]) > 2:
                    vino_data['bodega'] = f"{palabra} {palabras[i+1]}"
                else:
                    vino_data['bodega'] = palabra
                break
        
        return vino_data
    
    def extraer_vinos_pagina(self):
        """Extrae vinos de la página actual con múltiples estrategias"""
        print(f"🔍 Extrayendo vinos de página {self.pagina_actual}...")
        
        # Scroll inteligente
        self.scroll_inteligente()
        
        # Obtener HTML
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        
        vinos_encontrados = []
        
        # Estrategia 1: Enlaces directos a vinos (más confiable)
        print("   🎯 Estrategia 1: Enlaces directos a vinos...")
        enlaces_vino = soup.find_all('a', href=lambda x: x and '/w/' in str(x))
        
        urls_procesadas = set()
        
        for enlace in enlaces_vino:
            try:
                href = enlace.get('href')
                if not href:
                    continue
                
                # URL completa
                url_completa = href if href.startswith('http') else f"https://www.vivino.com{href}"
                
                # Evitar duplicados
                if url_completa in urls_procesadas:
                    continue
                urls_procesadas.add(url_completa)
                
                # Obtener texto del enlace y contenedores padre
                texto_enlace = enlace.get_text(strip=True)
                
                # Buscar contenedor padre con más información
                contenedor = enlace.find_parent(['div', 'article', 'li', 'section'])
                if contenedor:
                    texto_completo = contenedor.get_text(strip=True)
                else:
                    texto_completo = texto_enlace
                
                # Filtros de calidad
                if len(texto_completo) < 20:
                    continue
                
                if not ('€' in texto_completo or 'price' in texto_completo.lower()):
                    continue
                
                # Evitar enlaces de navegación
                if any(nav in texto_completo.lower() for nav in ['página', 'siguiente', 'anterior', 'filtro']):
                    continue
                
                # Extraer datos
                vino_data = self.extraer_datos_vino_avanzado(texto_completo, url_completa, len(vinos_encontrados) + 1)
                vinos_encontrados.append(vino_data)
                
                # Limitar para evitar sobrecarga
                if len(vinos_encontrados) >= 30:
                    break
                
            except Exception as e:
                print(f"   ⚠️ Error procesando enlace: {e}")
                continue
        
        print(f"✅ Extraídos {len(vinos_encontrados)} vinos de página {self.pagina_actual}")
        return vinos_encontrados
    
    def scraping_paginas_directas(self, url_base, max_paginas=5):
        """Realiza scraping navegando directamente a cada página por URL"""
        print(f"🚀 Iniciando scraping directo por páginas")
        print(f"🌐 URL base: {url_base}")
        print(f"📊 Máximo de páginas: {max_paginas}")
        
        total_vinos = 0
        
        for pagina in range(1, max_paginas + 1):
            self.pagina_actual = pagina
            print(f"\n📄 PROCESANDO PÁGINA {pagina}/{max_paginas}")
            
            # Navegar directamente a la página
            if not self.navegar_a_pagina(url_base, pagina):
                print(f"❌ No se pudo cargar página {pagina}. Continuando...")
                continue
            
            # Extraer vinos de la página
            vinos_pagina = self.extraer_vinos_pagina()
            
            if not vinos_pagina:
                print(f"⚠️ No se encontraron vinos en página {pagina}")
                if pagina > 1:  # Si es la primera página y no hay vinos, hay un problema
                    print("🔚 Finalizando scraping - no hay más contenido")
                    break
                continue
            
            # Agregar vinos extraídos
            self.datos_extraidos.extend(vinos_pagina)
            total_vinos += len(vinos_pagina)
            
            print(f"📊 Total acumulado: {total_vinos} vinos")
            
            # Pausa entre páginas
            if pagina < max_paginas:
                tiempo_pausa = 2 + random.uniform(1, 3)
                print(f"⏱️ Pausa de {tiempo_pausa:.1f}s antes de la siguiente página...")
                time.sleep(tiempo_pausa)
        
        print(f"\n✅ Scraping completado - Total de vinos: {len(self.datos_extraidos)}")
        return len(self.datos_extraidos) > 0
    
    def guardar_csv_multipagina(self):
        """Guarda los datos en archivos CSV"""
        try:
            carpeta = self.crear_carpeta_datos()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            headers = [
                'timestamp', 'session_id', 'pagina', 'posicion_pagina', 'posicion_global',
                'nombre_completo', 'url', 'precio_eur', 'precio_original', 'descuento',
                'bodega', 'region', 'año', 'rating', 'num_reviews', 'categoria_calidad',
                'tipo_vino', 'disponibilidad'
            ]
            
            # Archivo individual
            archivo_individual = f"{carpeta}/vivino_multipagina_{timestamp}.csv"
            with open(archivo_individual, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                for vino in self.datos_extraidos:
                    writer.writerow(vino)
            
            print(f"✅ CSV individual guardado: {archivo_individual}")
            
            # Archivo histórico
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
            print(f"❌ Error guardando CSV: {e}")
            return None, None
    
    def generar_reporte_final(self):
        """Genera reporte final del scraping multi-página"""
        if not self.datos_extraidos:
            print("⚠️ No hay datos para generar reporte")
            return
        
        print("\n" + "="*80)
        print("📊 REPORTE FINAL - SCRAPING MULTI-PÁGINA VIVINO")
        print("="*80)
        
        total_vinos = len(self.datos_extraidos)
        paginas_procesadas = len(set(v.get('pagina', 1) for v in self.datos_extraidos))
        
        print(f"🕐 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔑 Session ID: {self.session_id}")
        print(f"📄 Páginas procesadas: {paginas_procesadas}")
        print(f"🍷 Total de vinos: {total_vinos}")
        print(f"📊 Promedio por página: {total_vinos/paginas_procesadas:.1f} vinos")
        
        # Distribución por página
        print(f"\n📄 DISTRIBUCIÓN POR PÁGINA:")
        for pagina in sorted(set(v.get('pagina', 1) for v in self.datos_extraidos)):
            vinos_pag = len([v for v in self.datos_extraidos if v.get('pagina') == pagina])
            print(f"   Página {pagina}: {vinos_pag} vinos")
        
        # Análisis de precios
        precios = [v['precio_eur'] for v in self.datos_extraidos if v['precio_eur']]
        if precios:
            print(f"\n💶 ANÁLISIS DE PRECIOS:")
            print(f"   Vinos con precio: {len(precios)} ({len(precios)/total_vinos*100:.1f}%)")
            print(f"   Rango: €{min(precios):.2f} - €{max(precios):.2f}")
            print(f"   Promedio: €{sum(precios)/len(precios):.2f}")
        
        # Análisis de ratings
        ratings = [v['rating'] for v in self.datos_extraidos if v['rating']]
        if ratings:
            print(f"\n⭐ ANÁLISIS DE RATINGS:")
            print(f"   Vinos con rating: {len(ratings)} ({len(ratings)/total_vinos*100:.1f}%)")
            print(f"   Rating promedio: {sum(ratings)/len(ratings):.2f}")
        
        # Top regiones
        regiones = {}
        for v in self.datos_extraidos:
            if v['region']:
                regiones[v['region']] = regiones.get(v['region'], 0) + 1
        
        if regiones:
            print(f"\n🌍 TOP REGIONES:")
            for region, count in sorted(regiones.items(), key=lambda x: x[1], reverse=True)[:8]:
                print(f"   {region}: {count} vinos")
        
        print("="*80)
    
    def ejecutar_scraping_mejorado(self, url=None, max_paginas=5):
        """Ejecuta el proceso completo de scraping mejorado"""
        print("🚀 INICIANDO SCRAPING MULTI-PÁGINA MEJORADO")
        
        if not url:
            # URL por defecto con filtros para vinos españoles
            url = "https://www.vivino.com/explore?e=eJwFwUsKgCAUBdDd3GFEQp_BHbaBoFFEmBpIWtLru_vOsYmLDuIQD6qsRvQbK0T9ssxh2PYdEhVuQ-yHpXVisM8fZyfnlLxZBQ-3KwQ8Moxsih82Qhr5"
        
        if not self.configurar_driver():
            return False
        
        try:
            # Realizar scraping multi-página
            if not self.scraping_paginas_directas(url, max_paginas):
                return False
            
            # Guardar datos
            self.guardar_csv_multipagina()
            
            # Generar reporte
            self.generar_reporte_final()
            
            print("\n✅ SCRAPING MULTI-PÁGINA COMPLETADO EXITOSAMENTE")
            return True
            
        except Exception as e:
            print(f"❌ Error en proceso completo: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                print("🔚 Driver cerrado")


def main():
    """Función principal mejorada"""
    print("🍷 VIVINO SCRAPER MULTI-PÁGINA MEJORADO")
    print("=" * 50)
    
    # Configuración
    headless = True      # Cambiar a False para ver navegador
    max_paginas = 4      # Número de páginas a procesar
    
    # Crear y ejecutar scraper
    scraper = VivinoScraperMejorado(headless=headless)
    exito = scraper.ejecutar_scraping_mejorado(max_paginas=max_paginas)
    
    if exito:
        print("\n🎉 PROCESO COMPLETADO CON ÉXITO")
        print("📁 Revisa la carpeta 'datos_scraping' para los archivos CSV")
    else:
        print("\n❌ PROCESO FALLÓ - Revisa los errores anteriores")
    
    return exito


if __name__ == "__main__":
    main()
