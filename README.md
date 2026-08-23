# RepoMind

**The multi-agent operating system that lives entirely inside a GitHub repository.**

Issues = tasks.  
PRs = self-evolution.  
Actions = compute.  
Files + Wiki = memory.

Built phone-first from Saigon by a solo Grok/xAI builder.

## Why RepoMind exists
Most agent frameworks need servers, Docker, or a local machine.  
RepoMind turns the GitHub repo itself into the OS.

- Agents open Issues and PRs to improve their own code
- You drive everything from GitHub mobile
- Heavy modular skill packs (Crypto TA, X growth, self-improve)
- Native continuity with xlOS, Vesper contracts, grok-install, BbotBook

## Phone-First Workflow
1. Create an Issue describing the goal
2. Label it `task` / `agent` / `crypto` / `x-growth` / `self-improve`
3. Agents implement via comments / PRs
4. Review & merge on your phone
5. Scheduled Actions keep the swarm alive while you sleep

See `docs/phone-workflow.md` for details.

## Architecture
```
core/          agent base, orchestrator, GitHub client, safety, LLM, skill_loader
agents/        Critic, CryptoAnalyst, XGrowth, SelfImprove (+ base_runner)
skills/        modular skill packs (crypto TA, x_growth, self_improve)
contracts/     Vesper-style YAML constitutions & agent roles
memory/        persistent state + lessons
.github/       the actual runtime (Actions)
```

## Current Agents
- **Critic** (default) – safety & constitution reviews
- **CryptoAnalyst** – multi-asset TA scans (stub → real data later)
- **XGrowth** – high-signal thread & reply drafts
- **SelfImprove** – proposes modular improvements to the repo itself

## Current Status
**Phase 1h** – Four specialized agents registered and routing by labels.  
CI test workflow added. Skills cleaned.  
Ready for real data feeds and stronger LLM skill bodies once `XAI_API_KEY` is added.

## Quick Start (from phone)
1. Open an Issue and label it.
2. Watch the runner comment.
3. Review on mobile.

---
*RepoMind is part of the AgentMindCloud ecosystem.*
