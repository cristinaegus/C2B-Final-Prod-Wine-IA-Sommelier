# Despliegue de Flask en PythonAnywhere

## 1. Sube tu proyecto

1. Regístrate o inicia sesión en https://www.pythonanywhere.com/
2. Ve a la pestaña "Files" y sube tu proyecto (puedes comprimirlo en un .zip y descomprimirlo allí, o clonar desde GitHub usando la consola de PythonAnywhere).

## 2. Crea un entorno virtual (opcional pero recomendado)

En la consola de PythonAnywhere:

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configura la aplicación web

1. Ve a la pestaña "Web" y haz clic en "Add a new web app".
2. Elige "Manual configuration" y selecciona "Flask" y la versión de Python adecuada.
3. En "Source code", pon la ruta a tu carpeta del proyecto (por ejemplo: `/home/tu_usuario/tu_proyecto`).
4. En "WSGI configuration file", edita el archivo y reemplaza el contenido por algo como esto:

```python
import sys
import os

# Añade la ruta de tu proyecto
path = '/home/tu_usuario/tu_proyecto'
if path not in sys.path:
    sys.path.append(path)

# Activa el entorno virtual
activate_this = '/home/tu_usuario/tu_proyecto/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app_sommelier import app as application
```

## 4. Variables de entorno

- Si usas `.env`, configura las variables en la sección "Web" > "Environment Variables" o directamente en tu código.

## 5. Archivos estáticos

- En la sección "Static files", añade una línea para servir `/static/` desde la carpeta `static` de tu proyecto.

## 6. Reinicia la web app

- Haz clic en "Reload" en la parte superior de la pestaña "Web".

---

¡Listo! Tu app Flask debería estar accesible desde la URL que te da PythonAnywhere.

¿Quieres que te genere el contenido exacto para el archivo WSGI según tu ruta?
