from core.agent_base import AgentBase, AgentResult
from tools.repo_analyzer import analyze_repository


class RepositoryEngineerAgent(AgentBase):
    name = "repository_engineer_agent"

    def execute(self, task):
        root = "."
        if isinstance(task, dict):
            root = task.get("root", ".")
        report = analyze_repository(root)
        insight = f"missing_tests={report['missing_tests']} modules={report['modules']}"
        self.memory.store_repository_insight(repository=root, insight=insight, metadata={"tool": "repo_analyzer"})
        return AgentResult(agent=self.name, status="done", output="Repository analyzed", metadata=report)
