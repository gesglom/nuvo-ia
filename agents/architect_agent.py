from core.ollama_client import ask_llm


class ArchitectAgent:

    def execute(self, goal):

        prompt = f"""
Eres un arquitecto senior de software.

Tu tarea es diseñar la arquitectura del sistema.

Debes responder en español.

Incluye:

- arquitectura general
- estructura de carpetas
- módulos principales
- relación frontend backend

Objetivo del sistema:

{goal}
"""

        return ask_llm(prompt)

