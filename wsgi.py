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
