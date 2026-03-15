import os
import sys

sys.path.append(os.getcwd())

from agents.agent_creator import AgentCreatorAgent
from core.agent_loader import load_agents


def _safe_remove(path):
    if os.path.exists(path):
        os.remove(path)


def main():
    creator = AgentCreatorAgent()
    created = creator.create_specialist_agent("numpy optimization")
    name = created["agent"]

    after = set(load_agents().keys())
    print("created:", created)
    print("after:", sorted(after))

    if name not in after:
        raise SystemExit(f"ERROR: agente {name} no fue detectado por hot-loading")

    # Cleanup de prueba para no dejar basura en el repo
    _safe_remove(created["file"])
    _safe_remove(created["manifest"])

    print("OK: hot-loading validado")


if __name__ == "__main__":
    main()
