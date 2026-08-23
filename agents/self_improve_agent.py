"""Self-Improve agent – proposes small, safe improvements to the repo."""
from __future__ import annotations
from core.agent_base import BaseAgent
from core.models import AgentRole, Task, ActionResult

try:
    from skills.self_improve.code_evolver.implementation import run as evolve
except ImportError:
    def evolve(**kwargs):
        return {
            "proposal": "Stub: review recent Issues and suggest one small modular improvement.",
            "files": [],
            "rationale": "No implementation yet"
        }


class SelfImproveAgent(BaseAgent):
    def __init__(self, github=None, llm=None, **kwargs):
        role = AgentRole(
            name="self_improve",
            system_prompt="You are the Self-Improve agent of RepoMind. Propose small, safe, modular improvements. Prefer skills/ and agents/ over core/. Always respect the Constitution.",
            allowed_skills=["code_evolver"],
            max_iterations=3,
        )
        super().__init__(role=role, github=github, llm=llm, **kwargs)

    async def perceive(self, task: Task) -> dict:
        return {"title": task.title, "body": task.body, "issue": task.issue_number, "labels": task.labels}

    async def plan(self, perception: dict) -> list:
        return ["propose"]

    async def act(self, plan: list, task: Task) -> ActionResult:
        result = evolve(task=task.title, llm=self.llm)
        summary = (
            f"**Self-Improve proposal**\n\n"
            f"{result.get('proposal', 'No proposal')}\n\n"
            f"_Rationale: {result.get('rationale', '')}_\n\n"
            f"(Proposal only – create a draft PR or wait for human-approved label before any core change)"
        )
        if self.github:
            self.github.comment_on_issue(task.issue_number, summary)
        return ActionResult(success=True, summary=summary, output=result)
