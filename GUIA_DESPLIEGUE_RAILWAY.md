# Despliegue de la aplicación Flask en Railway

## 1. Prepara tu proyecto

Asegúrate de tener en la raíz de tu proyecto:

- `requirements.txt` (todas las dependencias, incluyendo Flask)
- `Procfile` con el siguiente contenido:
  ```
  web: python app_sommelier.py
  ```
- Si usas variables de entorno (.env), tenlas a mano para configurarlas en Railway.

## 2. Sube tu proyecto a GitHub

1. Crea un repositorio en GitHub (si no lo tienes).
2. Sube tu código al repositorio.

## 3. Despliega en Railway

1. Ve a https://railway.app/
2. Inicia sesión con tu cuenta de GitHub.
3. Haz clic en "New Project" > "Deploy from GitHub repo".
4. Selecciona tu repositorio.
5. Railway detectará el `Procfile` y el entorno Python automáticamente.
6. Configura las variables de entorno necesarias en la sección "Variables".
7. Haz clic en "Deploy".

## 4. Accede a tu aplicación

- Cuando el despliegue termine, Railway te dará una URL pública para tu app.
- Si usas base de datos, Railway puede crear una y te dará las variables de conexión.

## 5. Notas importantes

- Si tu app necesita escuchar en un puerto específico, usa la variable de entorno `PORT`:
  ```python
  import os
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
  ```
- Si tienes archivos estáticos o modelos grandes, considera almacenarlos en un bucket externo (S3, etc.)
- Railway tiene un plan gratuito con límites de uso.

---

¿Dudas? Consulta la documentación oficial: https://docs.railway.app/deploy/deployments/python
