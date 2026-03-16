import os
import sys

sys.path.append(os.getcwd())

from agent_loop import start_nuvo_flow
from core.llm_client import provider_status


def main():
    goal = "Crear base de backend y frontend con endpoint de health y estructura inicial"

    if not os.getenv("NUVO_LLM_PROVIDER"):
        os.environ["NUVO_LLM_PROVIDER"] = "localdev"

    print("Provider status:", provider_status())
    result = start_nuvo_flow(goal)
    print("Resultado final:", result.get("status"), "job_id=", result.get("job_id"))


if __name__ == "__main__":
    main()
