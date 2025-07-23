# Explicación del Funcionamiento del Sistema Wine IA

## 1. Descripción General

Wine IA es una aplicación web inteligente para la recomendación de vinos españoles. Utiliza algoritmos de Machine Learning y modelos de lenguaje (IA) para ofrecer recomendaciones personalizadas y un chatbot conversacional. El sistema está compuesto por un frontend moderno, un backend robusto en Flask y modelos de IA entrenados sobre datos reales de Vivino.

---

## 2. Estructura del Proyecto

- **Frontend:** HTML, CSS (Bootstrap, estilos propios), JavaScript.
- **Backend:** Python (Flask), SQLAlchemy, modelos IA, endpoints REST.
- **Modelos IA:** Clasificación de calidad de vinos, recomendación y chatbot Groq LLM.
- **Base de datos:** PostgreSQL (usuarios, recomendaciones).
- **Archivos principales:**
  - `app_sommelier.py`: Backend Flask principal.
  - `chatbot.py`: Lógica del chatbot Groq.
  - `templates/`: Archivos HTML (home, sommelier, about, login, register).
  - `static/`: Estilos CSS y modelos IA serializados.
  - `requirements.txt`: Dependencias Python.
  - `wine_model.pkl`, `wine_scaler.pkl`, `model_info.pkl`: Modelos IA y escaladores.

---

## 3. Procesos del Frontend

- **Interfaz de usuario:**
  - Navegación con Bootstrap.
  - Sección hero y características del sistema.
  - Formulario de recomendación Sommelier IA.
  - Widget de chatbot interactivo.
  - Animaciones y efectos visuales (parallax, contadores, IntersectionObserver).
- **Comunicación con el backend:**
  - Peticiones AJAX (fetch) para el chatbot (`/api/chatbot`).
  - Formularios para recomendaciones y registro/login.
  - Renderizado dinámico de resultados y mensajes.

---

## 4. Procesos del Backend

- **Inicialización:**
  - Carga de modelos IA y datos de vinos al iniciar la app.
  - Configuración de Flask y extensiones (SQLAlchemy, Bcrypt).
- **Endpoints principales:**
  - `/api/chatbot`: Recibe mensajes del usuario y responde usando Groq LLM.
  - `/api/vinos`: Devuelve lista de vinos del dataset.
  - `/api/recomendar`: Devuelve recomendaciones personalizadas según filtros.
  - `/register`, `/login`, `/logout`: Gestión de usuarios.
  - `/sommelier`: Página de recomendación con predicción de calidad y sugerencias.
  - `/about`: Información sobre el modelo y el sistema.
- **Procesos internos:**
  - Predicción de calidad de vino (funciones `predecir_calidad_vino_completo` y `predecir_calidad_vino_simple`).
  - Búsqueda y deduplicación de vinos similares (`buscar_vinos_similares`).
  - Validación y registro de usuarios.
  - Manejo de sesiones y autenticación.

---

## 5. Modelos de IA

- **Modelo de Clasificación de Vinos:**
  - Entrenado con datos de Vivino (precio, rating, año, bodega, región, popularidad).
  - Algoritmo principal: Random Forest Classifier.
  - Escalado y codificación de variables con `wine_scaler.pkl` y `model_info.pkl`.
  - Predicción de calidad y confianza.
- **Modelo de Recomendación:**
  - Filtrado y deduplicación avanzada de vinos según preferencias del usuario.
  - Estrategias de diversidad y calidad en la selección.
- **Chatbot Groq LLM:**
  - Integración con Groq API y modelo `llama3-8b-8192`.
  - Responde preguntas sobre vinos, recomendaciones y funcionamiento del sistema.
  - Endpoint `/api/chatbot` para comunicación frontend-backend.

---

## 6. Flujo de Usuario

1. El usuario accede a la web y navega por las secciones informativas.
2. Puede registrarse e iniciar sesión para guardar recomendaciones.
3. En la página Sommelier IA, ingresa sus preferencias y recibe recomendaciones personalizadas.
4. Puede interactuar con el chatbot para resolver dudas o pedir sugerencias.
5. El backend procesa las peticiones, consulta los modelos IA y responde con datos relevantes.

---

## 7. Seguridad y Buenas Prácticas

- Contraseñas cifradas con Bcrypt.
- Validación de datos en formularios.
- Manejo de sesiones seguras.
- Archivos sensibles y modelos ignorados en `.gitignore`.

---

## 8. Requisitos y Ejecución

- Instalar dependencias con `pip install -r requirements.txt`.
- Activar el entorno virtual y ejecutar `python app_sommelier.py`.
- Configurar variables de entorno (`GROQ_API_KEY`, conexión a base de datos).

---

## 9. Extensiones y Personalización

- Fácilmente ampliable con nuevos modelos IA o fuentes de datos.
- Personalización de estilos y textos en los archivos de `templates/` y `static/style/`.

---

## 10. Contacto y Créditos

- Proyecto desarrollado por cegusquiza.
- Basado en datos reales de Vivino y tecnologías modernas de IA.
