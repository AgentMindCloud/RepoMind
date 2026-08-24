"""Researcher agent – summarizes open Issues and repo activity (read-only)."""
from __future__ import annotations
from typing import List, Dict, Any
from core.agent_base import BaseAgent
from core.models import AgentRole, Task, ActionResult

class ResearcherAgent(BaseAgent):
    def __init__(self, github=None, skills=None, memory=None, llm=None, **kwargs):
        role = AgentRole(
            name="researcher",
            system_prompt=(
                "You are the Researcher agent of RepoMind. "
                "Your job is to summarize open Issues and recent activity. "
                "You are strictly read-only. Never change code or open PRs."
            ),
            allowed_skills=["research/issue_summarizer"],
            max_iterations=2,
            tools=["summarize", "comment"]
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
        return ["collect_open_issues", "summarize", "comment"]

    async def act(self, plan: list, task: Task) -> ActionResult:
        try:
            from skills.research.issue_summarizer.implementation import summarize_issues

            issues_data: List[Dict[str, Any]] = []
            if self.github:
                try:
                    open_tasks = self.github.get_open_tasks()
                    for t in open_tasks:
                        issues_data.append({
                            "number": t.issue_number,
                            "title": t.title,
                            "labels": t.labels or []
                        })
                except Exception as e:
                    issues_data = []
                    print(f"Could not fetch issues: {e}")

            result = summarize_issues(issues=issues_data)
            summary = result.get("summary", "No summary produced.")

            comment = (
                f"**ResearcherAgent** report\n\n"
                f"{summary}\n\n"
                f"**Next actions for you:**\n"
                f"- Pick an Issue and add the right agent label (`crypto`, `x-growth`, `self-improve`)\n"
                f"- Or create a new focused Issue\n"
            )

            if self.github:
                self.github.comment_on_issue(task.issue_number, comment)

            return ActionResult(
                success=True,
                summary=f"Summarized {result.get('count', 0)} open Issues",
                comments=[comment],
                output=result
            )
        except Exception as e:
            msg = f"**ResearcherAgent error**\n\n`{e}`"
            if self.github:
                try:
                    self.github.comment_on_issue(task.issue_number, msg)
                except Exception:
                    pass
            return ActionResult(success=False, summary=str(e))
