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
        return ["extract_topic", "choose_style", "generate_draft", "post_for_review"]

    async def act(self, plan: list, task: Task) -> ActionResult:
        try:
            from skills.x_growth.thread_factory.implementation import generate_thread, format_for_x
            topic = task.title
            for prefix in ["X Growth:", "Growth:", "Thread:"]:
                topic = topic.replace(prefix, "").strip()
            if not topic:
                topic = "RepoMind multi-agent OS"

            style = "solo-dev"
            labels = [l.lower() for l in task.labels]
            if "contrarian" in labels:
                style = "contrarian"
            elif "insight" in labels:
                style = "insight"
            elif "build-log" in labels or "log" in labels:
                style = "build-log"

            # Pass the live LLM client so the skill can use real Grok
            result = generate_thread(
                topic=topic,
                style=style,
                length=6,
                include_visuals=True,
                llm=self.llm
            )
            draft = format_for_x(result.get("thread", []))
            visuals = result.get("visual_ideas", [])
            used_llm = result.get("used_llm", False)

            comment = (
                f"**XGrowthAgent** draft ready for review  
"
                f"Style: `{style}` | LLM used: `{used_llm}`\n\n"
                f"```\n{draft}\n```\n\n"
            )
            if visuals:
                comment += "**Visual ideas:**\n" + "\n".join(f"- {v}" for v in visuals) + "\n\n"
            comment += (
                "**Next actions for you:**\n"
                "- Copy and post (or edit) the thread\n"
                "- Reply on this Issue if you want a different angle/style\n"
                "- Agents never auto-post\n\n"
                "*Human approval required before any live posting.*"
            )

            if self.github:
                self.github.comment_on_issue(task.issue_number, comment)
            return ActionResult(success=True, summary="Thread draft posted for review", output=result)
        except Exception as e:
            msg = f"XGrowthAgent error: {e}"
            if self.github:
                self.github.comment_on_issue(task.issue_number, msg)
            return ActionResult(success=False, summary=msg)
