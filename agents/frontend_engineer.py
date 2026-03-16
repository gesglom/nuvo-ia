from core.base_agent import BaseAgent
from core.memory_fabric import retrieve_context
from core.provider_router import route_llm


class FrontendEngineerAgent(BaseAgent):

    def execute(self, goal):
        context = retrieve_context(goal, agent="frontend_engineer")
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

Contexto reciente del proyecto:
{context}

Objetivo:
{goal}
"""

        return route_llm("frontend_engineer", prompt)
