"""Self-Improve Code Evolver – Phase 6."""
from typing import Dict, Any, List
from datetime import datetime, timezone

def evolve(focus: str = "general", task: str = "", llm=None, **kwargs) -> Dict[str, Any]:
    all_proposals: List[Dict[str, Any]] = [
        {
            "title": "Add 1h RSI column to CryptoTA",
            "why": "Faster timeframe context next to 4h/1d with low complexity.",
            "where": "skills/crypto/ta_scanner/implementation.py",
            "effort": "low",
            "priority": 1,
            "pr_ready": True,
            "patch_hint": "Fetch 1h klines, compute RSI(14), add column to markdown table.",
            "minimal_diff": (
                "# Additive sketch only – human must integrate carefully\n"
                "# closes_1h = _fetch_klines(sym, '1h', 100)\n"
                "# rsi_1h = _rsi(closes_1h) if closes_1h else None\n"
                "# include rsi_1h in table row / signals dict\n"
            ),
        },
        {
            "title": "Parse style/length hints in XGrowth Issue body",
            "why": "Users can write style:contrarian length:5 for matched drafts.",
            "where": "agents/x_growth_agent.py",
            "effort": "low",
            "priority": 2,
            "pr_ready": True,
            "patch_hint": "Regex extract style/length from task.body before generate_thread.",
            "minimal_diff": (
                "# import re\n"
                "# m = re.search(r'style\\s*:\\s*(\\w+)', (task.body or ''), re.I)\n"
                "# if m: style = m.group(1).lower()\n"
            ),
        },
        {
            "title": "Skill pack install Issue convention",
            "why": "Standardize `install pack <id>` Issues into draft PR updates of marketplace registry.",
            "where": "marketplace/registry.yaml",
            "effort": "low",
            "priority": 3,
            "pr_ready": True,
            "patch_hint": "Add/update pack status note when Issue requests install.",
        },
        {
            "title": "Persist useful confluence outcomes into LONG_TERM",
            "why": "Compound learning across runs without changing live trading behavior.",
            "where": "memory/LONG_TERM.md",
            "effort": "low",
            "priority": 4,
            "pr_ready": True,
        },
        {
            "title": "Satellite read-only status already exposed by Researcher",
            "why": "Keep cross-repo writes disabled; expand only with explicit human policy change.",
            "where": "core/multi_repo.py",
            "effort": "low",
            "priority": 5,
            "pr_ready": False,
        },
    ]

    if focus and focus.lower() != "general":
        focus_l = focus.lower()
        filtered = [
            p for p in all_proposals
            if focus_l in p["title"].lower() or focus_l in p["why"].lower() or focus_l in p["where"].lower()
        ]
        proposals = filtered or all_proposals[:4]
    else:
        proposals = all_proposals

    lines = ["## Self-Improve Proposals (Phase 6)\n"]
    for i, p in enumerate(proposals[:5], 1):
        pr_flag = "PR-ready" if p.get("pr_ready") else "proposal only"
        lines.append(
            f"**{i}. {p['title']}**  \n"
            f"_Effort: {p['effort']} | Priority: {p['priority']} | {pr_flag}_  \n"
            f"{p['why']}  \n"
            f"`{p['where']}`\n"
        )
    summary = "\n".join(lines)
    if task:
        summary = f"Context: {task[:120]}\n\n" + summary

    ts = datetime.now(timezone.utc)
    stamp = ts.strftime("%Y%m%d-%H%M%S")
    safe_files = {
        f"proposals/phase6-{stamp}.md": (
            f"# Self-Improve Proposal (Phase 6)\n\n"
            f"Generated: {ts.strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"Task: {task or 'n/a'}\nFocus: {focus}\n\n{summary}\n\n---\nDraft only.\n"
        )
    }

    top = proposals[0] if proposals else None
    if top and str(top.get("where", "")).startswith("skills/") and top.get("minimal_diff"):
        safe_files[f"proposals/patches/{stamp}-minimal.diff.md"] = (
            f"# Minimal gated patch sketch\n\n"
            f"Target: `{top['where']}`\n\n"
            f"```python\n{top['minimal_diff']}\n```\n\n"
            f"Human must integrate and test before merge.\n"
        )

    return {
        "proposals": proposals[:5],
        "proposal": proposals[0]["title"] if proposals else "No proposals",
        "summary": summary,
        "rationale": "Phase 6 priorities: real minimal gated patches, pack install convention, multi-repo status, compounding memory.",
        "safe_files": safe_files,
        "extra_files": safe_files,
        "version": "0.6.0",
        "timestamp": ts.isoformat(),
    }

def run(**kwargs) -> Dict[str, Any]:
    return evolve(**kwargs)
