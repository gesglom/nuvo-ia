import requests
import os


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"

WORKSPACE = "workspace/nuvo_backend"


class BackendEngineerAgent:

    def execute(self, goal):

        prompt = f"""
Eres un ingeniero backend experto en Python y FastAPI.

Debes crear archivos de backend.

Reglas:
- Siempre devuelve el resultado en este formato:

FILE: nombre_del_archivo.py
CODE:
codigo completo del archivo

Tarea:
{goal}
"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        return data.get("response", "")
