# RepoMind

**The multi-agent OS that lives entirely inside a GitHub repository.**

Issues = tasks.  
PRs = self-evolution.  
Actions = compute.  
Files + Wiki = memory.

Built from a phone in Saigon by a solo Grok/xAI builder.

## Why RepoMind
Most agent frameworks need servers, Docker, or local machines.  
RepoMind turns the GitHub repo itself into the operating system.

- Agents open Issues and PRs to improve their own code
- Drive everything from GitHub mobile
- Heavy skill packs for crypto TA, X growth, research, monetization
- Native continuity with xlOS, BbotBook, Vesper contracts, grok-install

## Phone-First Workflow
1. Open an Issue describing what you want
2. Label it (e.g. `task` or `agent`)
3. Agents run via Actions, comment results, open PRs
4. Review & merge on phone
5. The system improves itself

## Architecture
```
core/          – agent base, orchestrator, GitHub client, safety, llm
agents/        – specialized agents
skills/        – the heavy skill packs (CryptoTA, X-Growth, Self-Improve...)
contracts/     – Vesper-style YAML constitutions & roles
memory/        – persistent state
.github/       – the actual runtime (Actions)
dashboard/     – command center (later)
```

## Phase 1 Priority Skills
- CryptoTA-Heavy
- X-Growth-Swarm
- Self-Improve / Critic
- BbotBook-Integrator
- Researcher

## Status
Phase 0 scaffold live. Agents waking up.

## Quick Start (tomorrow with keys)
Add `XAI_API_KEY` secret → open Issue labeled `task` → watch the runner.
