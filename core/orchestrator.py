"""Orchestrator – routes tasks to specialized agents and enforces basic safety."""
from typing import Optional, Dict
from .models import Task, ActionResult, AgentRole
from .agent_base import BaseAgent
from .github_client import GitHubClient
from .llm import LLMClient
from .safety import SafetyGuard
from .skill_loader import SkillLoader

class Orchestrator:
    def __init__(self, github: Optional[GitHubClient] = None, llm: Optional[LLMClient] = None):
        self.github = github or GitHubClient()
        self.llm = llm or LLMClient()
        self.safety = SafetyGuard()
        self.skills = SkillLoader()
        self.agents: Dict[str, BaseAgent] = {}

        # Lazy registration of known agents
        self._register_default_agents()

    def _register_default_agents(self):
        try:
            from agents.critic_agent import CriticAgent
            self.register_agent("critic", CriticAgent(github=self.github, llm=self.llm))
            self.register_agent("default", CriticAgent(github=self.github, llm=self.llm))
        except Exception as e:
            print(f"Could not register CriticAgent: {e}")

        try:
            from agents.crypto_analyst_agent import CryptoAnalystAgent
            self.register_agent("crypto", CryptoAnalystAgent(github=self.github, llm=self.llm))
            self.register_agent("crypto_ta", CryptoAnalystAgent(github=self.github, llm=self.llm))
        except Exception as e:
            print(f"Could not register CryptoAnalystAgent: {e}")

        try:
            from agents.x_growth_agent import XGrowthAgent
            self.register_agent("x_growth", XGrowthAgent(github=self.github, llm=self.llm))
        except Exception as e:
            print(f"Could not register XGrowthAgent: {e}")

        try:
            from agents.self_improve_agent import SelfImproveAgent
            self.register_agent("self_improve", SelfImproveAgent(github=self.github, llm=self.llm))
        except Exception as e:
            print(f"Could not register SelfImproveAgent: {e}")

    def register_agent(self, name: str, agent: BaseAgent):
        self.agents[name] = agent

    def route_task(self, task: Task) -> str:
        labels = [l.lower() for l in task.labels]
        if any(x in labels for x in ["critic", "review", "safety"]):
            return "critic"
        if any(x in labels for x in ["crypto", "ta", "scan"]):
            return "crypto"
        if any(x in labels for x in ["x-growth", "growth", "thread", "x"]):
            return "x_growth"
        if any(x in labels for x in ["self-improve", "evolve", "improve"]):
            return "self_improve"
        if any(x in labels for x in ["agent", "task"]):
            return "critic"  # default to critic for safety on generic tasks
        return "critic"

    async def run_task(self, task: Task) -> ActionResult:
        agent_name = self.route_task(task)
        agent = self.agents.get(agent_name)

        if not agent:
            summary = f"No agent registered for route '{agent_name}'. Acknowledging task #{task.issue_number}."
            try:
                self.github.comment_on_issue(task.issue_number, f"**Orchestrator**: {summary}")
            except Exception:
                pass
            return ActionResult(success=True, summary=summary)

        result = await agent.run(task)

        # Always try to surface comments
        if result.comments and self.github:
            for c in result.comments:
                try:
                    self.github.comment_on_issue(task.issue_number, c)
                except Exception:
                    pass

        return result

    def run_task_sync(self, task: Task) -> ActionResult:
        import asyncio
        return asyncio.run(self.run_task(task))
