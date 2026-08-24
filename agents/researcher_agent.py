"""Researcher agent – summarizes open Issues + multi-repo status."""
from __future__ import annotations
from core.agent_base import BaseAgent
from core.models import AgentRole, Task, ActionResult

class ResearcherAgent(BaseAgent):
    def __init__(self, github=None, llm=None, **kwargs):
        role = AgentRole(
            name="researcher",
            system_prompt=(
                "You are the Researcher agent of RepoMind. "
                "Summarize open Issues, group them by label, and report multi-repo status. "
                "Read-only. Never change code."
            ),
            allowed_skills=["summarize_issues"],
            max_iterations=2,
        )
        super().__init__(role=role, github=github, llm=llm, **kwargs)

    async def perceive(self, task: Task) -> dict:
        return {"title": task.title, "body": task.body or "", "issue": task.issue_number, "labels": task.labels}

    async def plan(self, perception: dict) -> list:
        return ["summarize"]

    async def act(self, plan: list, task: Task) -> ActionResult:
        issues_data = []
        if self.github:
            try:
                tasks = self.github.get_open_tasks()
                issues_data = [
                    {"number": t.issue_number, "title": t.title, "labels": t.labels}
                    for t in tasks
                ]
            except Exception:
                issues_data = []

        by_label = {}
        for iss in issues_data:
            labels = iss.get("labels") or ["unlabeled"]
            for lab in labels:
                by_label.setdefault(lab, []).append(iss)

        lines = [f"### ResearcherAgent – Open Issues ({len(issues_data)} total)", ""]
        if not issues_data:
            lines.append("_No open Issues found or could not fetch them._")
        else:
            for lab, items in sorted(by_label.items(), key=lambda x: -len(x[1])):
                lines.append(f"**`{lab}`** ({len(items)})")
                for it in items[:6]:
                    lines.append(f"- #{it['number']} {it['title'][:70]}")
                if len(items) > 6:
                    lines.append(f"- … and {len(items)-6} more")
                lines.append("")

        # Multi-repo status (read-only)
        try:
            from core.multi_repo import multi_repo_status
            lines += ["### Multi-repo status", multi_repo_status(), ""]
        except Exception as e:
            lines += ["### Multi-repo status", f"_Unavailable: {e}_", ""]

        lines += [
            "**Next actions for you:**",
            "- Pick an Issue and label it `crypto`, `x-growth`, `self-improve`, or `research`",
            "- Or create a new Issue describing what you want done",
            "",
            "_Researcher is read-only._"
        ]

        comment = "\n".join(lines)
        if self.github:
            try:
                self.github.comment_on_issue(task.issue_number, comment)
            except Exception:
                pass

        return ActionResult(
            success=True,
            summary=f"Summarized {len(issues_data)} open Issues + multi-repo status",
            output={"count": len(issues_data), "by_label": {k: len(v) for k, v in by_label.items()}},
            comments=[comment]
        )
