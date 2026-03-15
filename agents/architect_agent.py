from core.base_agent import BaseAgent
from core.context_manager import summarize_recent
from core.provider_router import route_llm


class ArchitectAgent(BaseAgent):

    def execute(self, goal):
        context = summarize_recent()
        prompt = f"""
Eres un arquitecto senior de software.

Tu tarea es diseñar la arquitectura del sistema.

Debes responder en español.

Incluye:

- arquitectura general
- estructura de carpetas
- módulos principales
- relación frontend backend

Contexto reciente del proyecto:
{context}

Objetivo del sistema:

{goal}
"""

        return route_llm("architect_agent", prompt)
