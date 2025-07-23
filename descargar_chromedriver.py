import subprocess
import re
import requests
import zipfile
import io
import sys
import os

# Detectar versión de Chrome instalada
try:
    result = subprocess.run([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--version"], capture_output=True, text=True)
    chrome_version = result.stdout.strip()
except Exception:
    print("No se pudo detectar la versión de Chrome automáticamente. Ingresa la versión manualmente.")
    chrome_version = "138.0.7204.101" #input("Versión de Chrome (ejemplo: 138.0.7204.101): ")

match = re.search(r'(\d+\.\d+\.\d+)', chrome_version)
if not match:
    print("No se pudo extraer la versión principal de Chrome. Verifica la instalación.")
    sys.exit(1)

main_version = match.group(1).split('.')[0]
print(f"Versión principal detectada: {main_version}")

# Buscar la versión compatible de ChromeDriver
version_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{main_version}"
version_response = requests.get(version_url)
if version_response.status_code != 200:
    print("No se encontró ChromeDriver para tu versión de Chrome. Descárgalo manualmente desde https://chromedriver.chromium.org/downloads")
    sys.exit(1)

driver_version = version_response.text.strip()
print(f"Versión de ChromeDriver compatible: {driver_version}")

# Descargar el ChromeDriver correcto
BASE_URL = "https://chromedriver.storage.googleapis.com/"
CHROMEDRIVER_FILENAME = "chromedriver.exe"
CHROMEDRIVER_ZIP = "chromedriver_win32.zip"
download_url = f"{BASE_URL}{driver_version}/{CHROMEDRIVER_ZIP}"
print(f"Descargando desde: {download_url}")

response = requests.get(download_url)
if response.status_code != 200:
    print("Error al descargar ChromeDriver. Verifica la URL o tu conexión a internet.")
    sys.exit(1)

with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    z.extract(CHROMEDRIVER_FILENAME, os.getcwd())

print(f"✅ ChromeDriver descargado y extraído en: {os.path.join(os.getcwd(), CHROMEDRIVER_FILENAME)}")
print("Ya puedes ejecutar tu script con Selenium.")
