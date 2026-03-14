from core.agent_loader import load_agents
from core.ollama_client import ask_llm


def create_plan(goal, agents):

    agent_list = ", ".join(agents.keys())

    prompt = f"""
Eres el líder de un equipo de ingeniería de software.

Debes decidir qué agentes usar para cumplir un objetivo.

Agentes disponibles:

{agent_list}

Objetivo:

{goal}

Responde SOLO con una lista separada por comas de los agentes que deben ejecutarse.

Ejemplo:

architect_agent, backend_engineer, security_auditor
"""

    response = ask_llm(prompt)

    plan = [x.strip() for x in response.split(",")]

    return plan


def run_project(goal):

    print("\n===== NUVO AI PROJECT LEADER =====\n")

    agents = load_agents()

    print("Agentes detectados:")

    for name in agents:
        print("-", name)

    plan = create_plan(goal, agents)

    print("\nPlan generado:")

    for step in plan:
        print("-", step)

    for step in plan:

        agent = agents.get(step)

        if agent:

            print(f"\nEjecutando agente: {step}\n")

            result = agent.execute(goal)

            print(result)

        else:

            print(f"\nAgente no encontrado: {step}")


if __name__ == "__main__":

    goal = input("Describe el sistema que deseas crear: ")

    run_project(goal)

