"""Crypto Analyst agent – runs TA skills and comments results."""
from typing import Dict, Any, List
from core.agent_base import BaseAgent
from core.models import AgentRole, Task, ActionResult

class CryptoAnalystAgent(BaseAgent):
    def __init__(self, github=None, skills=None, memory=None, llm=None):
        role = AgentRole(
            name="crypto_analyst",
            system_prompt=(
                "You are the Crypto Analyst agent of RepoMind. "
                "Run multi-asset TA scans, produce clear confluence summaries, "
                "and always include the 'Not financial advice' disclaimer. "
                "Focus on BTC, ETH, SOL, SUI, XRP and related signals."
            ),
            allowed_skills=["crypto/ta_scanner"],
            max_iterations=3,
            tools=["scan", "comment"]
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
        return ["run_ta_scan", "format_and_comment"]

    async def act(self, plan: list, task: Task) -> ActionResult:
        try:
            from skills.crypto.ta_scanner.implementation import scan
            result = scan(symbols=["BTC", "ETH", "SOL", "SUI", "XRP", "XLM"], timeframes=["4h", "1d"])
            summary = result.get("summary", "Scan completed")
            live = result.get("live_prices", False)

            comment = (
                f"**CryptoAnalystAgent** report  
"
                f"Live prices: `{live}` | Version: `{result.get('version')}`\n\n"
                f"{summary}\n\n"
                f"**Next actions for you:**\n"
                f"- Reply if you want different symbols or a deeper dive\n"
                f"- This is research only – never trade solely on agent output\n"
            )
            if self.github:
                self.github.comment_on_issue(task.issue_number, comment)
            return ActionResult(success=True, summary="TA scan posted", output=result)
        except Exception as e:
            msg = f"CryptoAnalystAgent error: {e}"
            if self.github:
                try:
                    self.github.comment_on_issue(task.issue_number, msg)
                except Exception:
                    pass
            return ActionResult(success=False, summary=msg)
