# RepoMind

**The multi-agent operating system that lives entirely inside a GitHub repository.**

Issues = tasks.  
PRs = self-evolution.  
Actions = compute.  
Files + Wiki = memory.

Built phone-first by a solo Grok/xAI builder (@JanSol0s / AgentMindCloud).

## How to use it (30-second version)

1. Open an Issue  
2. Add a label (`crypto`, `x-growth`, `task`, `self-improve`…)  
3. Agent runs and comments the result  
4. Review on your phone or PC

**Full simple guide →** [docs/USAGE.md](docs/USAGE.md)

## Why RepoMind exists
Most agent frameworks need servers or a local machine.  
RepoMind turns the GitHub repo itself into the OS. You drive everything with Issues + labels.

## Current Agents
- **Critic** (default) – safety & constitution reviews
- **CryptoAnalyst** – multi-asset TA scans
- **XGrowth** – high-signal thread & reply drafts (never auto-posts)
- **SelfImprove** – proposes modular improvements to the repo itself

## Architecture
```
core/          runtime (orchestrator, LLM, GitHub client, safety)
agents/        Critic, CryptoAnalyst, XGrowth, SelfImprove
skills/        modular skill packs
contracts/     Constitution + role YAMLs
memory/        working + long-term state
.github/       the actual compute engine (Actions)
```

## Current Status
**Phase 1j** – System is live and tested with real `XAI_API_KEY`.  
Four agents registered and routing by labels. Clear usage docs added.

## Quick links
- [How to use](docs/USAGE.md)
- [Phone workflow](docs/phone-workflow.md)
- [Actions runner](https://github.com/AgentMindCloud/RepoMind/actions/workflows/agent-runner.yml)
- [Open Issues](https://github.com/AgentMindCloud/RepoMind/issues)

---
*Part of the AgentMindCloud ecosystem.*
