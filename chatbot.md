# Cómo conectar tu chatbot con Tavily

Para conectar tu chatbot con Tavily y aprovechar la búsqueda web en tiempo real, sigue estos pasos generales:

1. **Regístrate y obtén una API Key de Tavily**  
   Ve a https://www.tavily.com/ y regístrate. Obtén tu clave de API desde el panel de usuario.

2. **Instala el paquete de Tavily**  
   Si usas Python, instala el paquete oficial:

   ```
   pip install tavily-python
   ```

3. **Integra Tavily en tu backend Flask**  
   En tu archivo Python donde gestionas el chatbot (por ejemplo, en el endpoint `/api/chatbot`), importa y usa Tavily para obtener resultados web y pásalos como contexto al modelo LLM.

   Ejemplo básico:

   ```python
   from tavily import TavilyClient

   tavily = TavilyClient(api_key="TU_API_KEY")

   def buscar_web_tavily(query):
       results = tavily.search(query, max_results=3)
       return results  # Puedes formatear los resultados para tu LLM

   # En tu endpoint Flask:
   @app.route('/api/chatbot', methods=['POST'])
   def chatbot():
       user_message = request.json['message']
       web_results = buscar_web_tavily(user_message)
       # Incluye web_results en el prompt/contexto de tu LLM
       respuesta = tu_funcion_llm(user_message, contexto=web_results)
       return jsonify({'response': respuesta})
   ```

4. **Incluye los resultados de Tavily en el prompt del LLM**  
   Modifica la función que llama al modelo para que use los resultados de Tavily como contexto adicional.

5. **(Opcional) Usa un retriever de Langchain**  
   Si usas Langchain, puedes integrar Tavily como retriever:

   ```python
   from langchain.retrievers import TavilySearchAPIRetriever

   retriever = TavilySearchAPIRetriever(api_key="TU_API_KEY")
   docs = retriever.get_relevant_documents("tu consulta")
   ```

6. **Configura la variable de entorno para la API Key**  
   Es recomendable guardar la clave en una variable de entorno y cargarla con `os.environ`.

¿Quieres que te ayude a modificar tu endpoint Flask para integrar Tavily directamente? Si es así, dime si usas Langchain o solo código Python puro.
