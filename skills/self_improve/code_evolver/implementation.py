"""Self-Improve Code Evolver – Phase 2a (stronger, prioritized proposals)."""
from typing import Dict, Any, List

def evolve(focus: str = "general", task: str = "", llm=None) -> Dict[str, Any]:
    # High-value, ordered proposals for the current state of RepoMind
    all_proposals = [
        {
            "priority": "high",
            "area": "crypto/ta_scanner",
            "idea": "Add real OHLCV + funding rate (Binance public endpoints) and simple RSI/MACD confluence",
            "effort": "medium"
        },
        {
            "priority": "high",
            "area": "x_growth/thread_factory",
            "idea": "Pass LLMClient from XGrowthAgent so every draft uses real Grok by default",
            "effort": "low"
        },
        {
            "priority": "high",
            "area": "agents",
            "idea": "Make all agents include a clear 'Next actions for human' section in comments",
            "effort": "low"
        },
        {
            "priority": "medium",
            "area": "core/github_client",
            "idea": "Add create_pull_request helper that opens draft PRs from SelfImprove proposals",
            "effort": "medium"
        },
        {
            "priority": "medium",
            "area": "tests",
            "idea": "Add integration-style tests for skill contracts and routing",
            "effort": "medium"
        },
        {
            "priority": "medium",
            "area": "skills",
            "idea": "Create a Researcher skill that can summarize recent Issues + PRs",
            "effort": "medium"
        },
        {
            "priority": "low",
            "area": "docs",
            "idea": "Add a short 'Agent personality' section to each agent role YAML",
            "effort": "low"
        },
    ]

    if focus and focus.lower() != "general":
        filtered = [p for p in all_proposals if focus.lower() in p["area"].lower() or focus.lower() in p["idea"].lower()]
        proposals = filtered or all_proposals[:4]
    else:
        proposals = all_proposals

    # Build readable output
    lines = ["## Self-Improve Proposals\n"]
    for i, p in enumerate(proposals, 1):
        lines.append(f"{i}. **[{p['priority'].upper()}] {p['area']}**")
        lines.append(f"   {p['idea']}  
")
        lines.append(f"   Effort: {p['effort']}\n")

    summary = "\n".join(lines)
    if task:
        summary = f"Context from Issue: {task[:120]}\n\n" + summary

    return {
        "proposals": proposals,
        "proposal": proposals[0]["idea"] if proposals else "No proposals",
        "summary": summary,
        "rationale": "Prioritized by impact on the live multi-agent loop and phone-first usability.",
        "version": "0.2.0"
    }

def run(**kwargs) -> Dict[str, Any]:
    return evolve(**kwargs)
