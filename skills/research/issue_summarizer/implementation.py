"""Research skill – summarize open Issues and recent activity."""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def summarize_issues(issues: List[Dict[str, Any]] = None, max_items: int = 12) -> Dict[str, Any]:
    """Produce a clean markdown summary of open Issues."""
    issues = issues or []
    if not issues:
        return {
            "summary": "No open Issues found to summarize.",
            "count": 0,
            "version": "0.1.0"
        }

    by_label: Dict[str, List] = {}
    for iss in issues[:max_items]:
        labels = iss.get("labels") or ["unlabeled"]
        primary = labels[0] if labels else "unlabeled"
        by_label.setdefault(primary, []).append(iss)

    lines = [
        f"# RepoMind Issue Summary",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC",
        f"Open Issues considered: {len(issues)}",
        "",
    ]

    for label, group in sorted(by_label.items(), key=lambda x: -len(x[1])):
        lines.append(f"### {label} ({len(group)})")
        for iss in group:
            title = iss.get("title", "(no title)")
            num = iss.get("number", "?")
            lines.append(f"- #{num} {title}")
        lines.append("")

    lines += [
        "### Suggested next actions",
        "- Pick the highest-priority crypto or growth Issue and run the matching agent",
        "- Use `self-improve` on any Issue that needs a draft PR",
        "- Close or label completed work",
        "",
        "_Researcher is read-only. It never changes code._"
    ]

    return {
        "summary": "\n".join(lines),
        "count": len(issues),
        "by_label": {k: len(v) for k, v in by_label.items()},
        "version": "0.1.0"
    }

def run(issues: List[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
    return summarize_issues(issues=issues, **kwargs)
