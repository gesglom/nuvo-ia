from core.base_agent import BaseAgent
from core.memory_fabric import retrieve_context
from core.provider_router import route_llm


class BackendEngineerAgent(BaseAgent):

    def execute(self, goal):
        context = retrieve_context(goal, agent="backend_engineer")
        prompt = f"""
Eres un ingeniero backend experto en Python y FastAPI.

Debes crear archivos de backend.

Reglas:
- Siempre devuelve el resultado en este formato:

FILE: nombre_del_archivo.py
CODE:
codigo completo del archivo

Contexto reciente del proyecto:
{context}

Tarea:
{goal}
"""

        return route_llm("backend_engineer", prompt)
