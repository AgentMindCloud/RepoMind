"""Critic agent – reviews proposals and enforces Constitution."""
from typing import Dict, Any
from core.agent_base import BaseAgent
from core.models import AgentRole, Task, ActionResult

class CriticAgent(BaseAgent):
    def __init__(self, github=None, skills=None, memory=None, llm=None):
        role = AgentRole(
            name="critic",
            system_prompt=(
                "You are the Critic agent of RepoMind. "
                "Your job is to review proposed changes, check against the Constitution, "
                "and either approve, request changes, or block unsafe actions. "
                "Be strict on secrets, core/ modifications, and financial claims."
            ),
            allowed_skills=[],
            max_iterations=3,
            tools=["review", "comment"]
        )
        super().__init__(role, github, skills, memory, llm)

    async def perceive(self, task: Task) -> dict:
        return {
            "title": task.title,
            "body": task.body,
            "labels": task.labels,
            "issue_number": task.issue_number
        }

    async def plan(self, perception: dict) -> list:
        return ["review_constitution", "comment_feedback"]

    async def act(self, plan: list, task: Task) -> ActionResult:
        comments = []
        # Simple rule-based critic for Phase 1
        body_lower = (task.body or "").lower()
        risky = any(k in body_lower for k in ["api_key", "secret", "force push", "delete core"])
        if risky:
            comments.append("**Critic**: Potential safety issue detected. Please clarify or remove sensitive operations before proceeding.")
            success = False
            summary = "Blocked by Critic – safety review required"
        else:
            comments.append("**Critic**: Looks reasonable for Phase 1. Proceed with caution. Constitution checks passed at basic level.")
            success = True
            summary = "Critic approved (basic rules)"

        if self.github:
            for c in comments:
                self.github.comment_on_issue(task.issue_number, c)

        return ActionResult(success=success, summary=summary, comments=comments)
