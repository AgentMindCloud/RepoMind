# RepoMind

**The multi-agent OS that lives entirely inside a GitHub repository.**

Issues = tasks.  
PRs = self-evolution.  
Actions = compute.  
Files + Wiki = memory.

Built from a phone in Saigon by a solo Grok/xAI builder (@JanSol0s / AgentMindCloud).

## Why RepoMind
Most agent frameworks need servers, Docker, or local machines.  
RepoMind turns the GitHub repo itself into the operating system.

- Agents open Issues and PRs to improve their own code
- You review and drive everything from GitHub mobile
- Heavy skill packs for crypto TA, X growth, research, monetization, self-improvement
- Native continuity with xlOS, BbotBook, Vesper contracts, grok-install standards

## Current Status (Phase 1d)
- Core runtime complete (github_client, llm, safety, orchestrator, skill_loader)
- Specialized agents: **Critic**, **CryptoAnalyst**, **XGrowth**
- Skills live: Crypto TA Scanner, X Growth Thread Factory, Self-Improve Code Evolver
- Constitution + agent role contracts
- Workflow runs the base_runner on Issues labeled `task` or `agent`
- First Issue + tests started

## Phone-First Workflow
1. Open an Issue (or label existing) with `task` / `agent` / `crypto` / `growth`
2. Actions runner picks it up and routes to the right agent
3. Agent comments results or drafts
4. Review & merge on mobile
5. System improves itself over time

## Quick Start
1. Add secrets: `XAI_API_KEY` (required for real Grok calls), optional X keys
2. Open or label an Issue
3. Watch the agents work

## Architecture
```
core/          – runtime primitives
agents/        – Critic, CryptoAnalyst, XGrowth, ...
skills/        – modular heavy skills (SKILL.md + code)
contracts/     – Constitution + role YAMLs
memory/        – working + long-term state
.github/       – the compute layer
```

## License
Apache-2.0
