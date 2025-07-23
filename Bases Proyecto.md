🥇 IDEA: Asistente Sommelier Inteligente
🎯 Objetivo:
Ayudar al usuario a elegir el vino ideal según su presupuesto, gusto y ocasión, usando un modelo de recomendación + análisis de sentimiento.

🔍 ¿Cómo funciona?
📦 Inputs del usuario (en la web):
Presupuesto (ej: "10€ - 25€")

Gusto preferido (ej: seco, dulce, frutal, robusto)

Ocasión (ej: cena romántica, fiesta, regalo, etc.)

Opción para escribir un comentario de lo que le gusta

🧠 Modelo de Machine Learning detrás

1. Modelo de Recomendación Personalizada
   Usa filtrado híbrido:

Content-based: compara vinos según características (precio, variedad, reviews, etc.)

Collaborative filtering: aprende de otros usuarios con gustos similares

Técnicas: LightFM, SVD, o KNN sobre embeddings

2. Análisis de Sentimiento (opcional)
   Analiza los reviews de los vinos para:

Mejorar el ranking

Mostrar puntuaciones emocionales (por ejemplo: “Muy recomendado para cenas románticas”)

Modelo: DistilBERT o Naive Bayes para clasificar los reviews (positivo / negativo / neutro)

🖥️ Interfaz Web (frontend + integración)
🔘 Panel interactivo (tipo cuestionario)
Input con sliders para precio

Menú desplegable para tipo de ocasión

Input libre con texto: “Describe qué tipo de vino te gusta”

📋 Resultado
Top 3 recomendaciones personalizadas

Imagen del vino

Precio

Review destacado (extraído por análisis de sentimiento)

Frase tipo: “Perfecto para una noche especial” (generado del modelo)

Botón: “Ver más similares”

🧩 Extra
Botón “¿Por qué este vino?” → explica brevemente con base en el modelo ("Basado en tu preferencia por vinos frutales y tu presupuesto")

Opción de guardar vinos favoritos (si hay login)

🛠️ Stack tecnológico sugerido
Componente Herramienta
Backend ML Python (FastAPI o Flask)
Recomendador LightFM o Surprise

Proyecto Final

El objetivo del proyecto final es repasar los contenidos vistos a lo largo del curso, desde aquel lejano marzo, sirviendo para refrescar la memoria de todo lo que hemos visto de manera “modularizada”. Al trabajarlo todo como un proyecto final, aprenderemos a ver cómo se relacionan entre sí todos los conceptos vistos en el curso. Vamos a montar el rompecabezas.
Estos son algunos de los conceptos más importantes y que podemos reflejar en el proyecto.

Frontend

Podemos construir el frontend con Javascript (puro o con React) o Python (usar plantillas Jinja con Flask o Django)
Podemos dar responsividad al Frontend de manera que se adapte en los estilos a diferentes tamaños de pantalla (dispositivos)
Daremos formato a los formularios típicos de Signup, Login, Logout, Admin…
Se pueden usar los elementos principales de una interfaz de usuario, como barras de navegación, un footer…

Backend

Podemos usar cualquiera de las tecnologías vistas FastAPI, Flask, Django.

El usuario podrá darse de alta en nuestro servicio, permanecer logueado con JWT… Las contraseñas se guardarán hasheadas y en una base de datos (nube o sqlite). Podemos prever migraciones con un sistema de gestión de las mismas.
Algunos endpoints o páginas podrán ser exclusivos del Admin (por ejemplo, eliminar usuarios) otros del usuario logueado y otros de acceso general. En función de roles.
Gestionarelos la seguridad de los formularios.

Crearemos también testeos automáticos para facilitar el desarrollo.

IA integrada

Podemos usar cualquiera de los modelos entrenados en la parte de IA para dar algún servicio al usuario. ¿Quieres tasar tu piso o coche? ¿Quieres saber si esa seta es comestible? ¿Qué planta es esa? O una gráfica generada a partir de datos ¿Quieres ver los precios de las gasolineras más cercanas? Se puede usar cualquier modelo de Kaggle o HuggingFace que esté ya entrenado o hacerles un reentrenamiento o ajuste fino.
En la medida de lo posible, podemos intentar subir el modelo a una plataforma de alojamiento.
