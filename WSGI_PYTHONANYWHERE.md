# Archivo WSGI para PythonAnywhere

Copia y pega este contenido en tu archivo WSGI de PythonAnywhere, ajustando la ruta a tu usuario y carpeta de proyecto:

```python
import sys
import os

# Ruta absoluta a tu proyecto
path = '/home/Dell/PyhtonIA/Wine_IA_Production'
if path not in sys.path:
    sys.path.append(path)

# Activa el entorno virtual
activate_this = '/home/Dell/PyhtonIA/Wine_IA_Production/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app_sommelier import app as application
```

- Cambia `/home/Dell/PyhtonIA/Wine_IA_Production` si tu usuario o carpeta es diferente.
- Si tu entorno virtual tiene otro nombre, ajusta la ruta de `activate_this`.

Guarda y recarga tu web app en PythonAnywhere para aplicar los cambios.
