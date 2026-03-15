import os
import sys

sys.path.append(os.getcwd())

from core.agent_loader import load_agents


def main():
    agents = load_agents()
    print("agents:", sorted(agents.keys()))

    failures = []
    for name, agent in agents.items():
        try:
            out = str(agent.execute("smoke test"))
            print(f"OK {name}: {out[:80]}")
        except Exception as exc:
            failures.append((name, str(exc)))

    if failures:
        raise SystemExit(f"FAILURES: {failures}")

    print("OK: all agents smoke-tested")


if __name__ == "__main__":
    main()
