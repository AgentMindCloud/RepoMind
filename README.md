# RepoMind

**The multi-agent operating system that lives entirely inside a GitHub repository.**

Issues = tasks.  
PRs = self-evolution.  
Actions = compute.  
Files + memory = long-term state.

Built phone-first from Saigon by a solo Grok/xAI builder.

## How to use it (30 seconds)

1. Open or create an Issue.
2. Add a label: `task`, `crypto`, `x-growth`, or `self-improve`.
3. Comment `/run` (or just wait / re-add the label).
4. The matching agent comments back with a draft or analysis.

Full simple guide → [docs/USAGE.md](docs/USAGE.md)

## Current Agents
- **Critic** (default) – safety & constitution reviews
- **CryptoAnalyst** – live multi-asset scans + RSI confluence (Binance)
- **XGrowth** – high-signal thread drafts (LLM-powered)
- **SelfImprove** – ranked, concrete improvement proposals

## Current Status
**Phase 2c** – Real Grok power + live market data + RSI.  
CryptoTA now pulls Binance klines and calculates RSI(14) confluence.

## Architecture
```
core/          agent base, orchestrator, GitHub client, safety, LLM, skill_loader
agents/        Critic, CryptoAnalyst, XGrowth, SelfImprove (+ base_runner)
skills/        modular skill packs (crypto TA now with RSI)
contracts/     constitutions & agent roles
memory/        persistent state
.github/       the actual runtime (Actions)
```

---
*RepoMind is part of the AgentMindCloud ecosystem.*
