import requests
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"

AGENTS_DIR = "agents"


class AgentCreatorAgent:

    def execute(self, goal):

        prompt = f"""
Eres un ingeniero experto en sistemas de agentes IA.

Tu tarea es crear un nuevo agente Python.

Reglas:

El agente debe tener esta estructura:

class NombreDelAgente:

    def execute(self, goal):
        pass

El agente debe ser guardado como archivo .py.

Objetivo del nuevo agente:

{goal}

Responde SOLO con este formato:

FILE: nombre_agente.py
CODE:
codigo completo del archivo
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
