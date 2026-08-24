# RepoMind

**GitHub-native multi-agent OS**  
The repository *is* the runtime. Issues = tasks. Actions = compute. Agents evolve the system.

## Status: Phase 5a

Five specialized agents · live market data (incl. OI delta) · autonomous briefings · self-evolution · marketplace scaffolding.

| Agent         | What it does                                      |
|---------------|---------------------------------------------------|
| Critic        | Safety & constitution reviews                     |
| CryptoAnalyst | RSI + funding + volume + OI + **OIΔ**             |
| XGrowth       | High-signal X thread drafts (uses real Grok)      |
| SelfImprove   | Ranked proposals + draft PRs + skill notes        |
| Researcher    | Read-only summary of all open Issues              |

## How to use
1. Open/create an Issue  
2. Add a label (`crypto`, `x-growth`, `self-improve`, `research`, …)  
3. Comment `/run`  
4. Review agent output / draft PR

Full guide → [docs/USAGE.md](docs/USAGE.md)

## Autonomous features
- Daily briefing · Weekly X-Growth draft
- Draft PRs (never auto-merge)
- Marketplace skill-pack registry (scaffolding)
- Multi-repo readiness hooks

## Safety
- Human approval required for merges
- Safe-path file writes only
- Public market data only for crypto skill
