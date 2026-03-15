from core.base_agent import BaseAgent


class SecurityAuditorAgent(BaseAgent):
    def __init__(self):
        self.dangerous_commands = ["rm -rf", "eval", "os.system"]

    def scan_text(self, text):
        results = []
        for command in self.dangerous_commands:
            if command in text:
                results.append(f"Potential danger found: {command}")
        return results

    def execute(self, text):
        return self.scan_text(text)


if __name__ == "__main__":
    auditor = SecurityAuditorAgent()
    print("Auditor de Nuvo activo y verificado.")
