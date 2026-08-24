# RepoMind

**The multi-agent operating system that lives entirely inside a GitHub repository.**

Issues = tasks.  
PRs = self-evolution.  
Actions = compute.  
Files + memory = long-term state.

Built phone-first from Saigon by a solo Grok/xAI builder.

## How to use it (30 seconds)

1. Open or create an Issue.
2. Add a label: `task`, `crypto`, `x-growth`, `self-improve`, or `research`.
3. Comment `/run` (or Run workflow from Actions).
4. The matching agent comments back.

Full guide → [docs/USAGE.md](docs/USAGE.md)

## Current Agents
- **Critic** – safety & constitution reviews
- **CryptoAnalyst** – live Binance data + multi-TF RSI + funding + volume + OI
- **XGrowth** – LLM-powered thread drafts
- **SelfImprove** – ranked proposals + draft PRs with real files
- **Researcher** – summarizes open Issues

## Current Status
**Phase 4b** – Open Interest, weekly X-Growth drafts, stronger long-term memory, basic tests.

## Scheduled workflows
- Daily Briefing (crypto status)
- Weekly X-Growth Draft Issue (Monday)

## Architecture
```
core/          orchestrator, GitHub client, LLM, safety, skill loader
agents/        Critic, CryptoAnalyst, XGrowth, SelfImprove, Researcher
skills/        modular skill packs
.github/       Actions runtime
```

---
*RepoMind is part of the AgentMindCloud ecosystem.*
