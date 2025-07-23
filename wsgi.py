import sys
import os

# Ruta absoluta a tu proyecto en PythonAnywhere
path = '/home/cegusquiza/Wine_IA_Production'
if path not in sys.path:
    sys.path.append(path)

# Activa el entorno virtual (¡usa activate_this.py!)
activate_this = '/home/cegusquiza/Wine_IA_Production/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app_sommelier import app as application
