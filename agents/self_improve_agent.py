"""Self-Improve Agent – Phase 2b (structured, prioritized, phone-friendly)."""
from __future__ import annotations
from core.agent_base import BaseAgent
from core.models import AgentRole, Task, ActionResult
from core.skill_loader import SkillLoader

class SelfImproveAgent(BaseAgent):
    def __init__(self, github=None, skills=None, memory=None, llm=None, **kwargs):
        role = AgentRole(
            name="self_improve",
            system_prompt=(
                "You are the Self-Improve agent of RepoMind. "
                "Propose small, safe, modular improvements. "
                "Prefer skills/ and agents/ over core/. Always respect the Constitution. "
                "Never force-merge. Output clear, actionable, prioritized proposals."
            ),
            allowed_skills=["self_improve/code_evolver"],
            max_iterations=3,
            tools=["evolve", "comment"]
        )
        super().__init__(role, github, skills or SkillLoader(), memory, llm)

    async def perceive(self, task: Task) -> dict:
        return {
            "title": task.title,
            "body": task.body or "",
            "issue": task.issue_number,
            "labels": task.labels
        }

    async def plan(self, perception: dict) -> list:
        return ["call_code_evolver", "format_comment"]

    async def act(self, plan: list, task: Task) -> ActionResult:
        skill_fn = None
        if self.skills:
            try:
                skill_fn = self.skills.load_implementation("self_improve/code_evolver")
            except Exception:
                skill_fn = None

        focus = "general"
        text = f"{(task.body or '')} {task.title}".lower()
        if "test" in text:
            focus = "tests"
        elif "crypto" in text or "ta" in text:
            focus = "crypto"
        elif "x-growth" in text or "thread" in text or "growth" in text:
            focus = "x_growth"
        elif "agent" in text:
            focus = "agents"
        elif "core" in text:
            focus = "core"

        if skill_fn:
            result = skill_fn(focus=focus, task=task.title)
        else:
            # Fallback import
            try:
                from skills.self_improve.code_evolver.implementation import evolve
                result = evolve(focus=focus, task=task.title)
            except Exception as e:
                result = {
                    "proposal": f"Could not load evolver: {e}",
                    "proposals": [],
                    "summary": "Skill load failed",
                    "rationale": str(e)
                }

        # Build clean mobile-friendly comment
        lines = [
            f"**Self-Improve Agent** (focus: `{focus}`)",
            "",
            result.get("summary", "No summary generated."),
            "",
            f"_Rationale: {result.get('rationale', 'n/a')}_",
            "",
            "### Next actions for you",
            "1. Pick the highest-priority idea you like",
            "2. Reply on this Issue with ‘do #1’ or ‘do the crypto one’",
            "3. Or create a new Issue labeled `self-improve` with more context",
            "",
            "_Proposals only – nothing is changed until you approve._"
        ]

        comment = "\n".join(lines)

        if self.github:
            try:
                self.github.comment_on_issue(task.issue_number, comment)
            except Exception:
                pass

        return ActionResult(
            success=True,
            summary=result.get("summary", "Self-improve proposals generated")[:300],
            comments=[comment],
            output=result
        )
