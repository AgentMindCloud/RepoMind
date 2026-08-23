"""X Growth Thread Factory – magnetic threads optimized for solo AI/crypto builders."""
from typing import List, Dict, Any, Optional

HOOKS = {
    "solo-dev": [
        "Just shipped from Saigon:",
        "Building in public (phone-first):",
        "What I learned while the agents ran overnight:",
        "Solo builder log:",
    ],
    "contrarian": [
        "Everyone is overcomplicating AI agents.",
        "Stop building yet another local framework.",
        "The repo itself should be the OS.",
        "Most agent setups need servers. Ours doesn't.",
    ],
    "insight": [
        "The real unlock nobody talks about:",
        "After shipping multiple Grok agents I realized:",
        "Key insight from the trenches:",
    ],
    "build-log": [
        "Day of RepoMind:",
        "While I slept the Critic agent reviewed the code:",
        "Phone commit streak continues:",
    ]
}

def generate_thread(
    topic: str,
    style: str = "solo-dev",
    length: int = 6,
    include_visuals: bool = True
) -> Dict[str, Any]:
    """Generate a ready-to-post, scroll-stopping thread."""
    hooks = HOOKS.get(style, HOOKS["solo-dev"])
    hook = hooks[0]

    base_tweets = [
        f"{hook} {topic}",
        "2/ Context: I've been building a full multi-agent OS that lives *inside* a GitHub repo from my phone in Saigon.",
        "3/ Issues = the task board. PRs = how the agents evolve their own code. Actions = the compute engine.",
        "4/ No servers. No Docker. Just pure GitHub + Grok. The agents can open PRs to improve themselves.",
        "5/ This is RepoMind – open source, modular, and designed so a solo builder can drive everything from mobile.",
        "6/ Today's wave added Critic agent + expanded skills. The swarm is waking up.",
    ]

    if length > 6:
        base_tweets.append("7/ Next: real market data in the CryptoTA skill + live thread generation with Grok.")
    if length > 7:
        base_tweets.append("8/ If you're building agents or shipping from a phone, this architecture is worth stealing.")

    tweets = base_tweets[:max(3, min(length, 8))]

    # Soft CTA
    if not tweets[-1].endswith("?"):
        tweets[-1] += "\n\nWhat should the agents tackle next?"

    result = {
        "thread": tweets,
        "style": style,
        "topic": topic,
        "hooks": hooks,
        "version": "0.2.0",
        "disclaimer": "Draft only – human approval required before posting."
    }

    if include_visuals:
        result["visual_ideas"] = [
            "Screenshot of GitHub mobile showing the latest PR from an agent",
            "Code snippet of agent_base.py or orchestrator",
            "Simple meme: 'Local agent frameworks' vs 'The repo is the OS'",
            "Before/after of the file tree growth",
            "Phone in hand with the Issue list open"
        ]

    return result

def format_for_x(thread: List[str]) -> str:
    return "\n\n".join(thread)

def run(topic: str = "RepoMind self-improving agents", **kwargs) -> Dict[str, Any]:
    return generate_thread(topic, **kwargs)

if __name__ == "__main__":
    result = generate_thread("self-improving multi-agent OS inside GitHub", style="contrarian", length=7)
    print(format_for_x(result["thread"]))
    print("\nVisual ideas:", result.get("visual_ideas"))
