import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"


def diseñar_frontend(goal):

    prompt = f"""
Eres un ingeniero frontend experto.

Stack obligatorio:

Next.js (App Router)
React
TypeScript
Tailwind CSS

Tu tarea es diseñar el frontend.

Responde en español.

Debes devolver:

1) Estructura del proyecto frontend
2) Componentes React necesarios
3) Páginas de Next.js
4) Integración con API backend

Objetivo:
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
