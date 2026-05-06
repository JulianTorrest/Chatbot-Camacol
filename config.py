"""
Configuración del chatbot CAMACOL
"""
from enum import Enum

class AIModel(Enum):
    GEMINI = "gemini"
    DEEPSEEK = "deepseek"
    OPENAI = "openai"

# Versión de la aplicación
APP_VERSION = "1.1.0"
APP_NAME = "Chatbot CAMACOL"

# Configuración del chatbot
CHATBOT_NAME = "Asistente Virtual CAMACOL"
WELCOME_MESSAGE = "¡Hola! 👋 Soy el asistente virtual de CAMACOL. Estoy aquí para ayudarte con información sobre la Cámara Colombiana de la Construcción, servicios del sector constructor, normatividad, eventos y más. ¿En qué puedo ayudarte?"

# Configuración de proveedores de IA
AI_PROVIDERS = [
    {
        "name": "Google Gemini",
        "type": AIModel.GEMINI,
        "model": "gemini-1.5-flash",
        "api_key_env": "GOOGLE_API_KEY",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/models",
        "priority": 1,
        "free_tier": True
    },
    {
        "name": "DeepSeek",
        "type": AIModel.DEEPSEEK,
        "model": "deepseek-chat",
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com/v1",
        "priority": 2,
        "free_tier": True
    },
    {
        "name": "OpenAI GPT-4o-mini",
        "type": AIModel.OPENAI,
        "model": "gpt-4o-mini",
        "api_key_env": "OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1",
        "priority": 3,
        "free_tier": False
    }
]

# Enlaces útiles
LINKS = {
    "sitio_web": "https://camacol.co",
    "eventos": "https://camacol.co/eventos",
    "capacitacion": "https://camacol.co/capacitacion",
    "informacion": "https://camacol.co/informacion"
}

# Sugerencias de preguntas
SUGGESTED_QUESTIONS = [
    "¿Qué es CAMACOL?",
    "¿Cuáles son los servicios de CAMACOL?",
    "Información sobre el sector constructor",
    "¿Cómo puedo afiliarme?",
    "Eventos próximos de CAMACOL",
    "Estadísticas del sector constructor",
    "¿Qué normatividad aplica?",
    "Contacto de CAMACOL"
]

# Configuración de mensajes del sistema
SYSTEM_PROMPT = """Eres un asistente virtual experto de CAMACOL (Cámara Colombiana de la Construcción). 
Tu objetivo es ayudar a los usuarios con información precisa y útil sobre CAMACOL y el sector constructor en Colombia.

INSTRUCCIONES:
- Responde de manera amigable y profesional
- Si te preguntan sobre información específica de CAMACOL que no tienes en el contexto, dirígeles al sitio web oficial: www.camacol.co
- Proporciona información clara y concisa
- Responde en español colombiano
- Mantén un tono profesional pero cercano
- Si no estás seguro de algo, es mejor admitirlo y dirigir al usuario a la fuente oficial
"""

