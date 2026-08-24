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
- **CryptoAnalyst** – live Binance data + multi-TF RSI + funding + volume + OI + OIΔ
- **XGrowth** – LLM-powered thread drafts
- **SelfImprove** – ranked proposals + draft PRs with files / notes / patch templates
- **Researcher** – open Issues summary + multi-repo status

## Current Status
**Phase 6a** – Multi-repo status + skill-pack install scaffolding on top of Phase 5 complete system.

## Architecture
```
core/          orchestrator, GitHub client, multi-repo, LLM, safety
agents/        five specialized agents
skills/        modular skill packs
marketplace/   registry + install flow
config/        repos.yaml
.github/       Actions runtime
```

---
*RepoMind is part of the AgentMindCloud ecosystem.*
