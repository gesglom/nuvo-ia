import json
import requests

from core.agent_loader import load_agents
from core.project_scanner import scan_project
from core.memory_manager import add_completed_task
from core.git_manager import git_commit

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"


def ask_qwen(prompt):

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


def crear_plan(goal, agents):

    agent_list = "\n".join(agents.keys())

    prompt = f"""
Eres un arquitecto de software.

Divide este proyecto en tareas para agentes.

Proyecto:
{goal}

Agentes disponibles:
{agent_list}

Devuelve SOLO JSON así:

[
 {{"agent": "architect_agent", "task": "diseñar arquitectura"}},
 {{"agent": "backend_engineer", "task": "crear API"}},
 {{"agent": "frontend_engineer", "task": "crear interfaz"}}
]
"""

    result = ask_qwen(prompt)

    # limpiar markdown que devuelve el modelo
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:

        plan = json.loads(result)

        return plan

    except:

        print("Error interpretando plan")
        print(result)

        return []


def ejecutar_plan(plan, agents):

    for step in plan:

        agent_name = step["agent"]
        task = step["task"]

        print("\n=======================")
        print("AGENTE:", agent_name)
        print("TAREA:", task)

        if agent_name in agents:

            try:

                agents[agent_name].execute(task)

                add_completed_task(task)

                git_commit(f"AI completed task: {task}")

            except Exception as e:

                print("Error ejecutando agente:", e)

        else:

            print("Agente no encontrado")


def main():

    print("\n===== NUVO AI SYSTEM =====\n")

    agents = load_agents()

    print("Agentes cargados:")

    for a in agents:
        print("-", a)

    goal = input("\nObjetivo del proyecto: ")
    
    files = scan_project()

    print("\nArchivos del proyecto:")
    print(files)


    max_cycles = 5
    cycle = 0

    while cycle < max_cycles:

        print("\n=========== CICLO", cycle, "===========\n")

        plan = crear_plan(goal, agents)

        print("\nPLAN:\n", plan)

        ejecutar_plan(plan, agents)

        cycle += 1


if __name__ == "__main__":
    main()
