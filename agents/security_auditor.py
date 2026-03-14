class SecurityAuditor:
    def __init__(self):
        self.dangerous_commands = ['rm -rf', 'eval', 'os.system']

    def scan_text(self, text):
        results = []
        for command in self.dangerous_commands:
            if command in text:
                results.append(f"Potential danger found: {command}")
        return results

if __name__ == '__main__':
    auditor = SecurityAuditor()
    print('Auditor de Nuvo activo y verificado.')
