class BaseAgent:
    """Contrato base para todos los agentes de Nuvo."""

    name = "base_agent"

    def execute(self, goal):
        raise NotImplementedError("Cada agente debe implementar execute(goal)")
