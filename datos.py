from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify

def configurar_driver():
    """Configura el driver de Chrome para web scraping"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
    
    # Usar webdriver-manager para descargar automáticamente el ChromeDriver correcto
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def guardar_datos_csv(datos_vinos, precios):
    """Guarda los datos extraídos en un archivo CSV"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"vivino_scraping_{timestamp}.csv"
    
    try:
        # Crear directorio para los datos si no existe
        if not os.path.exists('datos_scraping'):
            os.makedirs('datos_scraping')
        
        ruta_archivo = os.path.join('datos_scraping', nombre_archivo)
        
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'nombre_vino', 'url', 'precio_eur', 'posicion']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Escribir encabezados
            writer.writeheader()
            
            # Escribir datos de vinos
            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for vino in datos_vinos:
                # Intentar extraer precio del nombre del vino
                precio_vino = None
                import re
                precio_match = re.search(r'(\d+[,.]?\d*)\s*€', vino['nombre'])
                if precio_match:
                    precio_vino = float(precio_match.group(1).replace(',', '.'))
                
                writer.writerow({
                    'timestamp': timestamp_str,
                    'nombre_vino': vino['nombre'],
                    'url': vino['url'],
                    'precio_eur': precio_vino,
                    'posicion': vino['posicion']
                })
        
        print(f"💾 Datos guardados en: {ruta_archivo}")
        return ruta_archivo
        
    except Exception as e:
        print(f"❌ Error al guardar CSV: {str(e)}")
        return None

def agregar_a_csv_historico(datos_vinos, precios):
    """Agrega los datos al archivo CSV histórico consolidado"""
    archivo_historico = "datos_scraping/vivino_historico.csv"
    
    try:
        # Crear directorio si no existe
        if not os.path.exists('datos_scraping'):
            os.makedirs('datos_scraping')
        
        # Verificar si el archivo existe para escribir encabezados
        archivo_existe = os.path.exists(archivo_historico)
        
        with open(archivo_historico, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'nombre_vino', 'url', 'precio_eur', 'posicion', 'session_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Escribir encabezados solo si es un archivo nuevo
            if not archivo_existe:
                writer.writeheader()
            
            # Crear ID único para esta sesión de scraping
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Escribir datos de vinos
            for vino in datos_vinos:
                # Intentar extraer precio del nombre del vino
                precio_vino = None
                import re
                precio_match = re.search(r'(\d+[,.]?\d*)\s*€', vino['nombre'])
                if precio_match:
                    precio_vino = float(precio_match.group(1).replace(',', '.'))
                
                writer.writerow({
                    'timestamp': timestamp_str,
                    'nombre_vino': vino['nombre'],
                    'url': vino['url'],
                    'precio_eur': precio_vino,
                    'posicion': vino['posicion'],
                    'session_id': session_id
                })
        
        print(f"📈 Datos agregados al historial: {archivo_historico}")
        return archivo_historico
        
    except Exception as e:
        print(f"❌ Error al agregar al CSV histórico: {str(e)}")
        return None


def guardar_datos_csv_completo(vinos_data, precios_adicionales):
    """Guarda datos completos de scraping en CSV individual con todos los campos"""
    try:
        # Crear carpeta si no existe
        carpeta_datos = "datos_scraping"
        if not os.path.exists(carpeta_datos):
            os.makedirs(carpeta_datos)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{carpeta_datos}/vivino_scraping_completo_{timestamp}.csv"
        
        # Encabezados expandidos para datos completos
        headers = [
            'timestamp', 'nombre_vino', 'url', 'precio_eur', 'posicion', 'session_id',
            'bodega', 'region', 'año', 'rating', 'num_reviews', 'categoria_calidad', 'tipo_vino'
        ]
        
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for vino in vinos_data:
                fila = [
                    timestamp_str,
                    vino.get('nombre', ''),
                    vino.get('url', ''),
                    vino.get('precio_eur', ''),
                    vino.get('posicion', ''),
                    session_id,
                    vino.get('bodega', ''),
                    vino.get('region', ''),
                    vino.get('año', ''),
                    vino.get('rating', ''),
                    vino.get('num_reviews', ''),
                    vino.get('categoria_calidad', ''),
                    vino.get('tipo_vino', '')
                ]
                writer.writerow(fila)
        
        print(f"✅ CSV completo guardado: {nombre_archivo}")
        return nombre_archivo
        
    except Exception as e:
        print(f"❌ Error al guardar CSV completo: {e}")
        return None


def agregar_a_csv_historico_completo(vinos_data, precios_adicionales):
    """Agrega datos completos al archivo CSV histórico"""
    try:
        carpeta_datos = "datos_scraping"
        if not os.path.exists(carpeta_datos):
            os.makedirs(carpeta_datos)
        
        archivo_historico = f"{carpeta_datos}/vivino_historico_completo.csv"
        
        # Verificar si el archivo existe para agregar encabezados
        archivo_existe = os.path.exists(archivo_historico)
        headers = [
            'timestamp', 'nombre_vino', 'url', 'precio_eur', 'posicion', 'session_id',
            'bodega', 'region', 'año', 'rating', 'num_reviews', 'categoria_calidad', 'tipo_vino'
        ]
        
        with open(archivo_historico, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Escribir encabezados solo si es un archivo nuevo
            if not archivo_existe:
                writer.writerow(headers)
            
            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for vino in vinos_data:
                fila = [
                    timestamp_str,
                    vino.get('nombre', ''),
                    vino.get('url', ''),
                    vino.get('precio_eur', ''),
                    vino.get('posicion', ''),
                    session_id,
                    vino.get('bodega', ''),
                    vino.get('region', ''),
                    vino.get('año', ''),
                    vino.get('rating', ''),
                    vino.get('num_reviews', ''),
                    vino.get('categoria_calidad', ''),
                    vino.get('tipo_vino', '')
                ]
                writer.writerow(fila)
        
        print(f"✅ CSV histórico completo actualizado: {archivo_historico}")
        return archivo_historico
        
    except Exception as e:
        print(f"❌ Error al actualizar CSV histórico completo: {e}")
        return None

def obtener_datos_vivino():
    """Función para hacer scraping completo de toda la página de Vivino"""
    driver = configurar_driver()
    try:
        url = "https://www.vivino.com/explore?e=eJwFwUsKgCAUBdDd3GFEQp_BHbaBoFFEmBpIWtLru_vOsYmLDuIQD6qsRvQbK0T9ssxh2PYdEhVuQ-yHpXVisM8fZyfnlLxZBQ-3KwQ8Moxsih82Qhr5"
        print(f"🌐 Accediendo a: {url}")
        
        driver.get(url)
        time.sleep(8)  # Esperar más tiempo para cargar completamente toda la página
        
        # Hacer scroll para cargar contenido dinámico
        print("📜 Haciendo scroll para cargar más contenido...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        print(f"📄 Página completa cargada, analizando todo el contenido...")
        
        # Estructura de datos más completa
        datos = {
            "mensaje": "Scraping completo de página Vivino realizado",
            "url_consultada": url,
            "timestamp_scraping": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "vinos": [],
            "metadatos": {
                "total_elementos_html": len(soup.find_all()),
                "total_enlaces": 0,
                "total_imagenes": 0,
                "filtros_aplicados": [],
                "regiones_encontradas": set(),
                "bodegas_encontradas": set(),
                "años_encontrados": set()
            },
            "estadisticas": {
                "total_vinos_encontrados": 0,
                "precios_promedio": [],
                "rating_promedio": 0,
                "precio_minimo": float('inf'),
                "precio_maximo": 0
            }
        }
        
        # 1. EXTRAER TODOS LOS ENLACES DE VINOS (sin límite)
        wine_links = soup.find_all('a', href=lambda x: x and '/w/' in str(x))
        print(f"🔗 Encontrados {len(wine_links)} enlaces de vinos en total")
        datos["metadatos"]["total_enlaces"] = len(wine_links)
        
        # 2. EXTRAER TODAS LAS IMÁGENES
        imagenes = soup.find_all('img')
        datos["metadatos"]["total_imagenes"] = len(imagenes)
        print(f"�️ Encontradas {len(imagenes)} imágenes")
        
        # 3. EXTRAER INFORMACIÓN DETALLADA DE CADA VINO
        vinos_procesados = set()  # Para evitar duplicados
        
        for i, link in enumerate(wine_links):
            href = link.get('href')
            if not href or href in vinos_procesados:
                continue
                
            vinos_procesados.add(href)
            text = link.text.strip()
            
            if href and text and len(text) > 10:  # Filtrar textos muy cortos
                # Extraer información detallada del texto del vino
                vino_info = {
                    "nombre": text,
                    "url": href if href.startswith('http') else f"https://www.vivino.com{href}",
                    "posicion": i + 1,
                    "bodega": "",
                    "region": "",
                    "año": None,
                    "rating": None,
                    "num_reviews": None,
                    "precio_eur": None,
                    "categoria_calidad": "",
                    "tipo_vino": ""
                }
                
                # Extraer información específica del texto
                import re
                
                # Extraer precio
                precio_match = re.search(r'(\d+[,.]?\d*)\s*€', text)
                if precio_match:
                    try:
                        precio = float(precio_match.group(1).replace(',', '.'))
                        vino_info["precio_eur"] = precio
                        datos["estadisticas"]["precios_promedio"].append(precio)
                        datos["estadisticas"]["precio_minimo"] = min(datos["estadisticas"]["precio_minimo"], precio)
                        datos["estadisticas"]["precio_maximo"] = max(datos["estadisticas"]["precio_maximo"], precio)
                    except:
                        pass
                
                # Extraer rating
                rating_match = re.search(r'(\d+[,.]?\d+)\s*\d+\s*valoraciones', text)
                if rating_match:
                    try:
                        rating = float(rating_match.group(1).replace(',', '.'))
                        vino_info["rating"] = rating
                    except:
                        pass
                
                # Extraer número de reviews
                reviews_match = re.search(r'(\d+)\s*valoraciones', text)
                if reviews_match:
                    try:
                        num_reviews = int(reviews_match.group(1))
                        vino_info["num_reviews"] = num_reviews
                    except:
                        pass
                
                # Extraer año
                año_match = re.search(r'(20\d{2}|19\d{2})', text)
                if año_match:
                    año = int(año_match.group(1))
                    vino_info["año"] = año
                    datos["metadatos"]["años_encontrados"].add(año)
                
                # Extraer región/país
                regiones = ['España', 'Francia', 'Italia', 'Portugal', 'Cataluña', 'Rioja', 'Madrid', 'Aragón', 
                           'Castilla', 'Extremadura', 'Campo de Borja', 'Calatayud', 'Terra Alta', 'Somontano',
                           'Empordà', 'Cariñena', 'Valdejalón']
                
                for region in regiones:
                    if region in text:
                        vino_info["region"] = region
                        datos["metadatos"]["regiones_encontradas"].add(region)
                        break
                
                # Extraer categoría de calidad
                calidades = ['Great Value', 'Good Value', 'Amazing Value', 'Cosecha más antigua']
                for calidad in calidades:
                    if calidad in text:
                        vino_info["categoria_calidad"] = calidad
                        break
                
                # Extraer bodega (primera palabra antes del nombre del vino)
                partes_texto = text.split()
                if len(partes_texto) > 0:
                    posible_bodega = partes_texto[0]
                    if len(posible_bodega) > 3 and not posible_bodega.isdigit():
                        vino_info["bodega"] = posible_bodega
                        datos["metadatos"]["bodegas_encontradas"].add(posible_bodega)
                
                datos["vinos"].append(vino_info)
        
        # 4. EXTRAER FILTROS Y METADATOS DE LA PÁGINA
        filtros = soup.find_all(['select', 'input', 'button'], class_=lambda x: x and 'filter' in str(x).lower())
        for filtro in filtros:
            if filtro.get('name') or filtro.get('id'):
                datos["metadatos"]["filtros_aplicados"].append({
                    "tipo": filtro.name,
                    "nombre": filtro.get('name', filtro.get('id')),
                    "valor": filtro.get('value', filtro.text.strip())[:50]
                })
        
        # 5. BUSCAR TODOS LOS PRECIOS EN LA PÁGINA
        todos_los_precios = soup.find_all(string=lambda x: x and '€' in str(x) and any(c.isdigit() for c in str(x)))
        precios_numericos = []
        for precio_texto in todos_los_precios:
            try:
                numeros = re.findall(r'(\d+[,.]?\d*)', precio_texto)
                for numero in numeros:
                    precio_num = float(numero.replace(',', '.'))
                    if 1 <= precio_num <= 2000:  # Rango más amplio para precios
                        precios_numericos.append(precio_num)
            except:
                continue
        
        # 6. CALCULAR ESTADÍSTICAS FINALES
        datos["estadisticas"]["total_vinos_encontrados"] = len(datos["vinos"])
        
        if datos["estadisticas"]["precios_promedio"]:
            datos["estadisticas"]["rating_promedio"] = sum([v["rating"] for v in datos["vinos"] if v["rating"]]) / len([v for v in datos["vinos"] if v["rating"]]) if [v for v in datos["vinos"] if v["rating"]] else 0
        
        if datos["estadisticas"]["precio_minimo"] == float('inf'):
            datos["estadisticas"]["precio_minimo"] = 0
        
        # Convertir sets a listas para JSON
        datos["metadatos"]["regiones_encontradas"] = list(datos["metadatos"]["regiones_encontradas"])
        datos["metadatos"]["bodegas_encontradas"] = list(datos["metadatos"]["bodegas_encontradas"])[:20]  # Limitar a 20
        datos["metadatos"]["años_encontrados"] = sorted(list(datos["metadatos"]["años_encontrados"]))
        
        # 7. GUARDAR DATOS EN CSV CON MÁS INFORMACIÓN
        archivo_guardado = guardar_datos_csv_completo(datos["vinos"], precios_numericos)
        archivo_historico = agregar_a_csv_historico_completo(datos["vinos"], precios_numericos)
        
        if archivo_guardado:
            datos["archivo_csv_generado"] = archivo_guardado
        if archivo_historico:
            datos["archivo_csv_historico"] = archivo_historico
        
        # Imprimir resumen completo
        print("\n" + "="*60)
        print("📊 SCRAPING COMPLETO DE PÁGINA VIVINO - RESULTADOS")
        print("="*60)
        print(f"🍷 Total de vinos únicos encontrados: {datos['estadisticas']['total_vinos_encontrados']}")
        print(f"💰 Total de precios extraídos: {len(precios_numericos)}")
        print(f"⭐ Rating promedio: {datos['estadisticas']['rating_promedio']:.2f}" if datos['estadisticas']['rating_promedio'] else "⭐ Rating promedio: N/A")
        print(f"� Rango de precios: {datos['estadisticas']['precio_minimo']:.2f}€ - {datos['estadisticas']['precio_maximo']:.2f}€")
        print(f"🌍 Regiones encontradas: {len(datos['metadatos']['regiones_encontradas'])} ({', '.join(datos['metadatos']['regiones_encontradas'][:5])}...)")
        print(f"� Bodegas encontradas: {len(datos['metadatos']['bodegas_encontradas'])}")
        print(f"📅 Años encontrados: {len(datos['metadatos']['años_encontrados'])} (desde {min(datos['metadatos']['años_encontrados']) if datos['metadatos']['años_encontrados'] else 'N/A'} hasta {max(datos['metadatos']['años_encontrados']) if datos['metadatos']['años_encontrados'] else 'N/A'})")
        print(f"🔗 Total de enlaces procesados: {datos['metadatos']['total_enlaces']}")
        print(f"🖼️ Total de imágenes: {datos['metadatos']['total_imagenes']}")
        
        if archivo_guardado:
            print(f"💾 CSV individual: {archivo_guardado}")
        if archivo_historico:
            print(f"� CSV histórico actualizado: {archivo_historico}")
        
        if datos["vinos"]:
            print(f"\n🍷 TOP 10 VINOS ENCONTRADOS:")
            for i, vino in enumerate(datos["vinos"][:10], 1):
                precio_str = f" - {vino['precio_eur']}€" if vino['precio_eur'] else ""
                rating_str = f" (⭐{vino['rating']})" if vino['rating'] else ""
                año_str = f" {vino['año']}" if vino['año'] else ""
                print(f"{i:2d}. {vino['bodega']}{año_str}{precio_str}{rating_str}")
                print(f"     {vino['region']} - {vino['categoria_calidad']}")
        
        print("="*60)
        
        return datos
        
    except Exception as e:
        error_msg = f"Error al obtener datos completos: {str(e)}"
        print(f"❌ {error_msg}")
        return {"error": error_msg}
    finally:
        driver.quit()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("wine_index.html")

@app.route("/api/datos", methods=["GET"])
def obtener_datos():
    """Endpoint para obtener datos de Vivino via scraping"""
    datos = obtener_datos_vivino()
    return jsonify(datos)

if __name__ == "__main__":
    print("🚀 Iniciando aplicación Flask Wine-IA-Web...")
    print("📡 Servidor disponible en: http://127.0.0.1:5000")
    print("🔗 API de datos: http://127.0.0.1:5000/api/datos")
    app.run(debug=True)