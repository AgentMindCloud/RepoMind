"""Self-Improve Agent – Phase 2e (can open real draft PRs)."""
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
                "Never force-merge. You may open *draft* PRs only."
            ),
            allowed_skills=["self_improve/code_evolver"],
            max_iterations=3,
            tools=["evolve", "comment", "create_draft_pr"]
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
        text = f"{perception.get('title','')} {perception.get('body','')}".lower()
        wants_pr = any(w in text for w in ["pr", "pull request", "draft", "implement", "open pr", "create pr"])
        return ["call_code_evolver", "format_comment", "maybe_open_draft_pr"] if wants_pr else ["call_code_evolver", "format_comment"]

    async def act(self, plan: list, task: Task) -> ActionResult:
        # Load skill
        try:
            from skills.self_improve.code_evolver.implementation import evolve
        except Exception as e:
            evolve = None
            result = {"summary": f"Could not load evolver: {e}", "proposals": [], "rationale": str(e)}

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

        if evolve:
            result = evolve(focus=focus, task=task.title)

        summary_md = result.get("summary", "No proposals generated.")
        rationale = result.get("rationale", "n/a")

        # Decide whether to open a draft PR
        wants_pr = any(w in text for w in ["pr", "pull request", "draft", "implement", "open pr", "create pr"])
        pr_url = None

        if wants_pr and self.github and hasattr(self.github, "create_draft_pr_from_proposal"):
            try:
                pr_body = (
                    f"## Self-Improve Draft PR\n\n"
                    f"Triggered by Issue #{task.issue_number}: **{task.title}**\n\n"
                    f"{summary_md}\n\n"
                    f"### Safety\n"
                    f"- This is a **draft** PR only\n"
                    f"- No automatic merge\n"
                    f"- Requires human review + `human-approved` label before any merge to main\n\n"
                    f"### Rationale\n{rationale}\n"
                )
                pr_url = self.github.create_draft_pr_from_proposal(
                    title=f"[Self-Improve] {task.title[:60]}",
                    body=pr_body,
                    branch_prefix="self-improve"
                )
            except Exception as e:
                pr_url = f"(failed to open draft PR: {e})"

        # Build comment
        lines = [
            f"**Self-Improve Agent** (focus: `{focus}`)",
            "",
            summary_md,
            "",
            f"_Rationale: {rationale}_",
            "",
        ]

        if pr_url and pr_url.startswith("http"):
            lines += [
                f"### Draft PR opened",
                f"→ {pr_url}",
                "",
                "Review the draft PR. Nothing will be merged until you approve.",
                "",
            ]
        elif pr_url:
            lines += [f"### Draft PR attempt", str(pr_url), ""]

        lines += [
            "### Next actions for you",
            "1. Review the proposals (and the draft PR if one was opened)",
            "2. Reply with ‘implement #1’ or similar if you want more work",
            "3. Add `human-approved` only when you are ready for a real merge",
            "",
            "_Agents never force-merge. Draft PRs only._"
        ]

        comment = "\n".join(lines)

        if self.github:
            try:
                self.github.comment_on_issue(task.issue_number, comment)
            except Exception:
                pass

        return ActionResult(
            success=True,
            summary=(summary_md[:200] + (f" | Draft PR: {pr_url}" if pr_url else "")),
            comments=[comment],
            output={"result": result, "pr_url": pr_url}
        )
