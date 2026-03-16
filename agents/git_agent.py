from core.agent_base import AgentBase, AgentResult
from tools.git_tools import create_commit, detect_changes, stage_changes


class GitAgent(AgentBase):
    name = "git_agent"

    def execute(self, task):
        message = "feat(factory): autonomous update"
        if isinstance(task, dict):
            message = task.get("commit_message", message)
        status = detect_changes()
        if not status.get("stdout"):
            return AgentResult(agent=self.name, status="noop", output="No changes to commit")
        stage_changes()
        commit = create_commit(message)
        return AgentResult(agent=self.name, status="done", output=str(commit))
