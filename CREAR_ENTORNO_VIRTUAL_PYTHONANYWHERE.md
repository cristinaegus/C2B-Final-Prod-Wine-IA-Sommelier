# Crear y usar un entorno virtual en PythonAnywhere

1. **Abre una consola Bash en PythonAnywhere**

2. **Crea el entorno virtual** (ajusta la versión de Python si es necesario):

```bash
python3.10 -m venv venv
```

3. **Activa el entorno virtual:**

```bash
source venv/bin/activate
```

4. **Instala tus dependencias:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. **Configura tu archivo WSGI** para que apunte a este entorno virtual (como ya tienes en tu ejemplo):

```python
activate_this = '/home/tu_usuario/tu_proyecto/venv/bin/activate_this.py'
```

6. **Recarga tu web app** desde la pestaña "Web" en PythonAnywhere.

---

**Notas:**

- No necesitas crear el entorno virtual en tu PC y subirlo; es mejor crearlo directamente en PythonAnywhere.
- Si ya tienes un requirements.txt actualizado, todo tu entorno se replicará correctamente.
- Si instalas nuevas dependencias, recuerda ejecutar `pip install ...` dentro del entorno virtual en PythonAnywhere.

¿Necesitas ayuda con algún paso concreto?
