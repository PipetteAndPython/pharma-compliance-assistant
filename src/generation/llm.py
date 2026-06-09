# =========================
# LLM INTERFACE (GROQ)
# =========================
# Módulo encargado de la generación de respuestas usando Groq

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# =========================
# CLIENTE GROQ
# =========================

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY no está configurada. Ejecutá: export GROQ_API_KEY='tu-key'")

client = Groq(api_key=api_key)

# =========================
# GENERACIÓN DE RESPUESTA
# =========================

def generate_answer(prompt):
    """
    Envía el prompt al LLM y devuelve la respuesta generada.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente técnico especializado en documentos "
                    "farmacéuticos y regulatorios. "
                    "Responde únicamente usando la información del contexto proporcionado."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content