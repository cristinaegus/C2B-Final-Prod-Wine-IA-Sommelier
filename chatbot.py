import os
from flask import Flask, request, jsonify
import requests
# Cargar variables de entorno desde .env automáticamente
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def load_model():
    from langchain.chat_models import init_chat_model
    return init_chat_model("llama3-8b-8192", model_provider="groq")

# Inicializar modelo Groq
from langchain_groq import ChatGroq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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 ").strip()
try:
    chat = ChatGroq(api_key=GROQ_API_KEY, model_name="llama3-8b-8192")
except Exception as e:
    print(f"Error inicializando ChatGroq: {e}")
    chat = None




## Elimina la lógica de búsqueda Grq, solo deja el chatbot
def chatbot_endpoint(chat):
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'response': 'Mensaje vacío'}), 400
    if chat is None:
        return jsonify({'response': 'Error: El modelo Groq no se ha inicializado correctamente.'}), 500
    try:
        from langchain_core.messages import HumanMessage
        prompt = f"Usuario: {user_message}\nResponde de forma útil, breve y profesional."
        response = chat.invoke([HumanMessage(content=prompt)])
        return jsonify({'response': str(getattr(response, 'content', response))})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500

## Elimina la simulación de endpoint Grq, ya no existe
