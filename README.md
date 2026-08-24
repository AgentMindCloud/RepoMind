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
- **SelfImprove** – ranked proposals + draft PRs + human-approved checklist + pack install
- **Researcher** – open Issues summary + multi-repo status

## Current Status
**Phase 8a** – CI hygiene (green tests), real pack checksum verification helpers, multi-repo policy tests.

## Scheduled workflows
- Daily Briefing
- Weekly X-Growth Draft

## Architecture
```
core/          orchestrator, GitHub client, multi-repo, LLM, safety
agents/        five specialized agents
skills/        modular skill packs
marketplace/   registry + signed packs + checksum helpers
config/        repos.yaml
.github/       Actions runtime
```

---
*RepoMind is part of the AgentMindCloud ecosystem.*
