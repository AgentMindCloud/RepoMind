"""Crypto Analyst agent – runs TA skills and posts clear structured comments."""
from typing import Dict, Any, List
from core.agent_base import BaseAgent
from core.models import AgentRole, Task, ActionResult

class CryptoAnalystAgent(BaseAgent):
    def __init__(self, github=None, skills=None, memory=None, llm=None):
        role = AgentRole(
            name="crypto_analyst",
            system_prompt=(
                "You are the Crypto Analyst agent of RepoMind. "
                "Run multi-asset TA scans with live Binance data + RSI, produce clear confluence summaries, "
                "and always include the 'Not financial advice' disclaimer."
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

            text = f"{task.title} {task.body or ''}".upper()
            candidates = ["BTC", "ETH", "SOL", "SUI", "XRP", "XLM", "BNB", "DOGE", "ADA", "AVAX"]
            found = [s for s in candidates if s in text]
            symbols = found if found else ["BTC", "ETH", "SOL", "SUI", "XRP"]

            result = scan(symbols=symbols)
            summary = result.get("summary", "Scan completed")
            live = result.get("live_prices", False)
            has_rsi = result.get("has_rsi", False)

            comment = (
                f"### CryptoAnalystAgent Report\n\n"
                f"Live data: `{live}` | RSI: `{has_rsi}` | Version: `{result.get('version')}`\n\n"
                f"{summary}\n\n"
                f"**Next actions for you:**\n"
                f"- Reply with different symbols if you want a custom scan\n"
                f"- This is research only – never trade solely on agent output\n"
            )

            if self.github:
                self.github.comment_on_issue(task.issue_number, comment)

            return ActionResult(
                success=True,
                summary="Live TA + RSI scan posted",
                output=result,
                comments=[comment]
            )
        except Exception as e:
            msg = f"**CryptoAnalystAgent error**\n\n`{e}`\n\nCheck Actions logs for details."
            if self.github:
                try:
                    self.github.comment_on_issue(task.issue_number, msg)
                except Exception:
                    pass
            return ActionResult(success=False, summary=str(e))
