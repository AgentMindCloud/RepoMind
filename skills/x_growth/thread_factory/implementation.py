"""X Growth Thread Factory – magnetic threads for solo AI/crypto builders.

LLM-aware: uses real Grok when an LLMClient is passed and XAI_API_KEY is present.
Falls back to strong templates otherwise.
"""
from typing import List, Dict, Any, Optional
import os

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

def _template_thread(topic: str, style: str = "solo-dev", length: int = 6) -> List[str]:
    hooks = HOOKS.get(style, HOOKS["solo-dev"])
    hook = hooks[0]
    base = [
        f"{hook} {topic}",
        "2/ Context: I've been building a full multi-agent OS that lives *inside* a GitHub repo from my phone in Saigon.",
        "3/ Issues = the task board. PRs = how the agents evolve their own code. Actions = the compute engine.",
        "4/ No servers. No Docker. Just pure GitHub + Grok. The agents can open PRs to improve themselves.",
        "5/ This is RepoMind – open source, modular, and designed so a solo builder can drive everything from mobile.",
        "6/ The swarm is awake. Critic, Crypto, X-Growth and Self-Improve agents are live.",
    ]
    if length > 6:
        base.append("7/ Next: real market data + fully dynamic Grok threads.")
    if length > 7:
        base.append("8/ If you're building agents or shipping from a phone, steal this architecture.")
    tweets = base[:max(3, min(length, 8))]
    if not tweets[-1].endswith("?"):
        tweets[-1] += "\n\nWhat should the agents tackle next?"
    return tweets

def generate_thread(
    topic: str,
    style: str = "solo-dev",
    length: int = 6,
    include_visuals: bool = True,
    llm=None,
) -> Dict[str, Any]:
    """Generate a ready-to-post thread. Uses Grok when llm client is provided."""
    used_llm = False
    tweets: List[str] = []

    api_key = os.getenv("XAI_API_KEY")
    if api_key and llm is not None:
        try:
            system = (
                "You are a high-signal X (Twitter) growth expert writing in the voice of a solo AI/crypto builder "
                "living in Saigon. Write short, punchy, numbered threads. No fluff. Strong hooks. "
                "Always end with a soft CTA question. Keep each tweet under 280 characters. Output only the tweets."
            )
            user = (
                f"Write a {length}-tweet thread about: {topic}\n"
                f"Style: {style}\n"
                f"Voice: authentic solo builder, phone-first, GitHub-native multi-agent OS called RepoMind."
            )
            content = llm.chat_sync([
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ], temperature=0.75, max_tokens=1200)

            lines = [l.strip() for l in content.replace("\r", "").split("\n") if l.strip()]
            # Clean common numbering artifacts
            cleaned = []
            for line in lines:
                for prefix in ["1/", "2/", "3/", "4/", "5/", "6/", "7/", "8/", "1.", "2.", "3.", "4.", "5.", "6."]:
                    if line.startswith(prefix):
                        line = line[len(prefix):].strip()
                        break
                cleaned.append(line)
            tweets = cleaned[:length]
            used_llm = True
        except Exception as e:
            print(f"LLM thread generation failed, falling back to template: {e}")
            tweets = _template_thread(topic, style, length)
    else:
        tweets = _template_thread(topic, style, length)

    result = {
        "thread": tweets,
        "style": style,
        "topic": topic,
        "version": "0.3.0",
        "used_llm": used_llm,
        "disclaimer": "Draft only – human approval required before posting."
    }

    if include_visuals:
        result["visual_ideas"] = [
            "Screenshot of GitHub mobile showing the latest agent comment",
            "Code snippet of the orchestrator or skill",
            "Meme: Local agent frameworks vs The repo is the OS",
            "Before/after of the file tree",
            "Phone in hand with Issues open"
        ]

    return result

def format_for_x(thread: List[str]) -> str:
    return "\n\n".join(thread)

def run(topic: str = "RepoMind self-improving agents", **kwargs) -> Dict[str, Any]:
    return generate_thread(topic, **kwargs)

if __name__ == "__main__":
    result = generate_thread("self-improving multi-agent OS inside GitHub", style="contrarian", length=6)
    print(format_for_x(result["thread"]))
    print("\nUsed LLM:", result.get("used_llm"))
