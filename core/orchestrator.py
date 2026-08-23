"""Simple orchestrator – routes tasks to agents."""
from typing import Optional, List
from .models import Task, ActionResult, AgentRole
from .agent_base import BaseAgent
from .github_client import GitHubClient
from .llm import LLMClient
from .safety import SafetyGuard

class Orchestrator:
    def __init__(self, github: Optional[GitHubClient] = None, llm: Optional[LLMClient] = None):
        self.github = github or GitHubClient()
        self.llm = llm or LLMClient()
        self.safety = SafetyGuard()
        self.agents: dict[str, BaseAgent] = {}

    def register_agent(self, name: str, agent: BaseAgent):
        self.agents[name] = agent

    def route_task(self, task: Task) -> Optional[str]:
        """Simple label-based routing."""
        labels = [l.lower() for l in task.labels]
        if any("crypto" in l or "ta" in l for l in labels):
            return "crypto"
        if any("x-growth" in l or "growth" in l or "x" in l for l in labels):
            return "x_growth"
        if any("self-improve" in l or "evolve" in l for l in labels):
            return "self_improve"
        if any("agent" in l or "task" in l for l in labels):
            return "default"
        return "default"

    async def run_task(self, task: Task) -> ActionResult:
        agent_name = self.route_task(task)
        agent = self.agents.get(agent_name)
        if not agent:
            # Fallback: comment and return
            summary = f"No specialized agent registered for '{agent_name}'. Scaffold acknowledges task #{task.issue_number}."
            self.github.comment_on_issue(task.issue_number, summary)
            return ActionResult(success=True, summary=summary)

        result = await agent.run(task)
        if result.comments:
            for c in result.comments:
                self.github.comment_on_issue(task.issue_number, c)
        return result

    def run_task_sync(self, task: Task) -> ActionResult:
        import asyncio
        return asyncio.run(self.run_task(task))
