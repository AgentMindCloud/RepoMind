"""X Growth agent – generates high-signal thread drafts for @JanSol0s style."""
from typing import Dict, Any
from core.agent_base import BaseAgent
from core.models import AgentRole, Task, ActionResult

class XGrowthAgent(BaseAgent):
    def __init__(self, github=None, skills=None, memory=None, llm=None):
        role = AgentRole(
            name="x_growth",
            system_prompt=(
                "You are the X Growth agent of RepoMind. "
                "Generate authentic, high-engagement thread drafts in the voice of a solo Grok/xAI builder from Saigon. "
                "Never auto-post. Always draft and request human approval."
            ),
            allowed_skills=["x_growth/thread_factory"],
            max_iterations=3,
            tools=["generate_thread", "comment"]
        )
        super().__init__(role, github, skills, memory, llm)

    async def perceive(self, task: Task) -> dict:
        return {
            "title": task.title,
            "body": task.body or "",
            "labels": task.labels,
            "issue_number": task.issue_number
        }

    async def plan(self, perception: dict) -> list:
        return ["extract_topic", "generate_draft", "post_for_review"]

    async def act(self, plan: list, task: Task) -> ActionResult:
        try:
            from skills.x_growth.thread_factory.implementation import generate_thread
            topic = task.title.replace("X Growth:", "").strip() or task.title
            result = generate_thread(topic=topic, goal="growth", tone="builder")
            draft = result.get("draft", "")
            comment = (
                f"**XGrowthAgent** draft ready for review:\n\n"
                f"```\n{draft}\n```\n\n"
                f"*Human approval required before any live posting.*"
            )
            if self.github:
                self.github.comment_on_issue(task.issue_number, comment)
            return ActionResult(success=True, summary="Thread draft posted for review", output=result)
        except Exception as e:
            msg = f"XGrowthAgent error: {e}"
            if self.github:
                self.github.comment_on_issue(task.issue_number, msg)
            return ActionResult(success=False, summary=msg)
