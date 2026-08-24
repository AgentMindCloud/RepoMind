"""Self-Improve Code Evolver – Phase 4a."""
from typing import Dict, Any
from datetime import datetime, timezone

def evolve(focus: str = "general", task: str = "", llm=None) -> Dict[str, Any]:
    all_proposals = [
        {
            "priority": "high",
            "area": "skills/crypto/ta_scanner",
            "idea": "Add 1h RSI column next to 4h/1d for shorter-term context",
            "effort": "low",
        },
        {
            "priority": "high",
            "area": "agents/self_improve_agent",
            "idea": "When focus=crypto, attach a suggested SKILL.md micro-bump in the draft PR",
            "effort": "medium",
        },
        {
            "priority": "medium",
            "area": "core",
            "idea": "Optional multi-repo config: list secondary repos for future orchestration",
            "effort": "medium",
        },
        {
            "priority": "medium",
            "area": ".github/workflows",
            "idea": "Weekly X-Growth draft Issue (manual approval still required before posting)",
            "effort": "medium",
        },
        {
            "priority": "medium",
            "area": "tests",
            "idea": "Add symbol-extraction unit tests for CryptoAnalyst",
            "effort": "low",
        },
        {
            "priority": "low",
            "area": "docs",
            "idea": "Phase 4 architecture notes for multi-repo readiness",
            "effort": "low",
        },
    ]

    if focus and focus.lower() != "general":
        filtered = [p for p in all_proposals if focus.lower() in p["area"].lower() or focus.lower() in p["idea"].lower()]
        proposals = filtered or all_proposals[:4]
    else:
        proposals = all_proposals

    lines = ["## Self-Improve Proposals (Phase 4)\n"]
    for i, p in enumerate(proposals, 1):
        lines.append(f"{i}. **[{p['priority'].upper()}] {p['area']}**")
        lines.append(f"   {p['idea']}  ")
        lines.append(f"   Effort: {p['effort']}\n")

    summary = "\n".join(lines)
    if task:
        summary = f"Context: {task[:120]}\n\n" + summary

    ts = datetime.now(timezone.utc)
    stamp = ts.strftime("%Y%m%d-%H%M%S")

    safe_files = {
        f"proposals/phase4-{stamp}.md": (
            f"# Self-Improve Proposal (Phase 4)\n\n"
            f"Generated: {ts.strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"Task: {task or 'n/a'}\nFocus: {focus}\n\n"
            f"{summary}\n\n"
            f"---\nDraft only. Requires human review before merge.\n"
        )
    }

    return {
        "proposals": proposals,
        "proposal": proposals[0]["idea"] if proposals else "No proposals",
        "summary": summary,
        "rationale": "Phase 4 priorities: OI confluence, gated skill edits, multi-repo readiness, scheduled growth drafts.",
        "safe_files": safe_files,
        "extra_files": safe_files,
        "version": "0.4.0",
        "timestamp": ts.isoformat(),
    }

def run(**kwargs) -> Dict[str, Any]:
    return evolve(**kwargs)
