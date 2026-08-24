"""Self-Improve Agent – Phase 6 (draft PRs + notes + patch templates + minimal sketches + pack install)."""
from __future__ import annotations
from core.agent_base import BaseAgent
from core.models import AgentRole, Task, ActionResult
from core.skill_loader import SkillLoader
from datetime import datetime, timezone
import re

FOCUS_SKILL_MD = {
    "crypto": "skills/crypto/ta_scanner/SKILL.md",
    "x_growth": "skills/x_growth/thread_factory/SKILL.md",
    "research": "skills/research/issue_summarizer/SKILL.md",
}

class SelfImproveAgent(BaseAgent):
    def __init__(self, github=None, skills=None, memory=None, llm=None, **kwargs):
        role = AgentRole(
            name="self_improve",
            system_prompt=(
                "You are the Self-Improve agent of RepoMind. "
                "Propose small, safe, modular improvements. Prefer skills/ and marketplace/ over core/. "
                "Never force-merge. Draft PRs only. Attach gated patch templates and minimal sketches."
            ),
            allowed_skills=["self_improve/code_evolver"],
            max_iterations=3,
            tools=["evolve", "comment", "create_draft_pr"]
        )
        super().__init__(role, github, skills or SkillLoader(), memory, llm)

    async def perceive(self, task: Task) -> dict:
        return {"title": task.title, "body": task.body or "", "issue": task.issue_number, "labels": task.labels}

    async def plan(self, perception: dict) -> list:
        text = f"{perception.get('title','')} {perception.get('body','')}".lower()
        wants_pr = any(w in text for w in [
            "pr", "pull request", "draft", "implement", "open pr", "create pr", "patch", "install pack"
        ])
        return ["call_code_evolver", "format_comment", "maybe_open_draft_pr"] if wants_pr else ["call_code_evolver", "format_comment"]

    async def act(self, plan: list, task: Task) -> ActionResult:
        result = {"summary": "No proposals", "proposals": [], "rationale": "n/a", "extra_files": {}}
        focus = "general"
        text = f"{(task.body or '')} {task.title}".lower()
        try:
            from skills.self_improve.code_evolver.implementation import evolve
            if "crypto" in text or "ta" in text:
                focus = "crypto"
            elif "x-growth" in text or "thread" in text or "growth" in text:
                focus = "x_growth"
            elif "research" in text or "status" in text:
                focus = "research"
            elif "test" in text:
                focus = "tests"
            elif "agent" in text:
                focus = "agents"
            elif "core" in text:
                focus = "core"
            result = evolve(focus=focus, task=task.title, llm=self.llm)
        except Exception as e:
            result = {"summary": f"Could not load evolver: {e}", "proposals": [], "rationale": str(e), "extra_files": {}}

        summary_md = result.get("summary", "No proposals generated.")
        rationale = result.get("rationale", "n/a")
        proposals = result.get("proposals", [])
        evolver_files = result.get("extra_files") or result.get("safe_files") or {}
        wants_pr = any(w in text for w in [
            "pr", "pull request", "draft", "implement", "open pr", "create pr", "patch", "install pack"
        ])
        pr_url = None
        install_match = re.search(r"install\s+pack\s+([a-z0-9_\-]+)", text)

        if wants_pr and self.github and (proposals or install_match):
            try:
                ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
                extra = {}
                if isinstance(evolver_files, dict):
                    extra.update(evolver_files)
                extra[f"memory/self_improve_runs/{ts}.md"] = (
                    f"# Self-Improve run {ts}\n\nIssue #{task.issue_number}\nFocus: {focus}\nPhase: 6\n"
                )
                skill_path = FOCUS_SKILL_MD.get(focus)
                if skill_path:
                    note_path = skill_path.replace("SKILL.md", "IMPROVE_NOTES.md")
                    extra[note_path] = (
                        f"# Improve Notes – {skill_path}\n\n## {ts}\nFocus: `{focus}`\n\n{summary_md[:1000]}\n\n_Draft only._\n"
                    )
                if install_match:
                    pack_id = install_match.group(1)
                    extra[f"marketplace/pending_installs/{ts}-{pack_id}.md"] = (
                        f"# Pending skill pack install\n\n"
                        f"Pack ID: `{pack_id}`\n"
                        f"Requested via Issue #{task.issue_number}\n"
                        f"Status: pending human review\n\n"
                        f"See marketplace/install.md for the safe install path.\n"
                    )
                if not any(k.startswith("proposals/patches/") for k in extra):
                    extra[f"proposals/patches/{ts}.md"] = (
                        f"# Gated Code Patch Template – {ts}\n\n"
                        f"Issue: #{task.issue_number} – {task.title}\nFocus: {focus}\n\n"
                        f"## Direction\n\n{summary_md[:1200]}\n\n"
                        f"### Safety\n- Draft PR only\n- Never auto-applied to main\n- Prefer minimal diffs under skills/\n"
                    )
                pr_body = (
                    f"## Self-Improve Draft PR (Phase 6)\n\n"
                    f"Triggered by Issue #{task.issue_number}: **{task.title}**\n\n{summary_md}\n\n"
                    f"### Safety\n- **Draft** only\n- Includes proposals, patch templates/sketches, optional IMPROVE_NOTES, optional pending install notes\n"
                    f"- Safe paths only\n\n### Rationale\n{rationale}\n"
                )
                pr_url = self.github.create_draft_pr_from_proposal(
                    title=f"[Self-Improve] {task.title[:60]}",
                    body=pr_body,
                    branch_prefix="self-improve",
                    extra_files=extra,
                )
            except Exception as e:
                pr_url = f"(failed to open draft PR: {e})"

        lines = [f"**Self-Improve Agent** (focus: `{focus}` · Phase 6)", "", summary_md, "", f"_Rationale: {rationale}_", ""]
        if pr_url and isinstance(pr_url, str) and pr_url.startswith("http"):
            lines += [
                "### Draft PR opened (proposals + patch templates/sketches)",
                f"→ {pr_url}",
                "",
                "Review carefully. Nothing merges until you approve.",
                "",
            ]
        elif pr_url:
            lines += ["### Draft PR attempt", str(pr_url), ""]
        lines += [
            "### Next actions for you",
            "1. Review proposals and files under proposals/patches/",
            "2. For pack installs, review marketplace/pending_installs/ and marketplace/install.md",
            "3. Add `human-approved` only when ready to merge",
            "",
            "_Agents never force-merge. Draft PRs only._",
        ]
        comment = "\n".join(lines)
        if self.github:
            try:
                self.github.comment_on_issue(task.issue_number, comment)
            except Exception:
                pass
        return ActionResult(
            success=True,
            summary=(summary_md[:180] + (f" | PR: {pr_url}" if pr_url else "")),
            comments=[comment],
            output={"result": result, "pr_url": pr_url},
        )
