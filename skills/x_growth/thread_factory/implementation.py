"""X Growth Thread Factory – Phase 1.5."""
from typing import List, Dict, Any

def generate_thread(topic: str, angle: str = "", length: int = 6) -> Dict[str, Any]:
    """Returns a structured draft thread. Full LLM version activates with XAI_API_KEY."""
    base = [
        f"1/ Building in public from Saigon → {topic}",
        f"2/ Angle: {angle or 'practical Grok agents + real distribution'}",
        "3/ Most agent frameworks need servers. We put the OS inside the GitHub repo itself.",
        "4/ Issues = tasks. PRs = evolution. Actions = compute. Files = memory.",
        "5/ This is RepoMind – the multi-agent OS you can drive from your phone.",
        "6/ Daily commits. Self-improving. Open source. Follow for the build."
    ]
    posts = base[:max(3, min(length, 8))]

    return {
        "thread": posts,
        "rationale": "Structured placeholder. Will call Grok for real high-signal threads once XAI_API_KEY is present.",
        "disclaimer": "Draft only – human approval required before any live posting.",
        "version": "0.1.5"
    }

def run(**kwargs) -> Dict[str, Any]:
    return generate_thread(**kwargs)
