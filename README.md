# RepoMind

**GitHub-native multi-agent OS**  
The repository *is* the runtime. Issues = tasks. Actions = compute. Agents evolve the system.

## Status: Phase 3 Complete

Five specialized agents + autonomous daily briefing + self-evolution via draft PRs.

| Agent         | What it does                                      |
|---------------|---------------------------------------------------|
| Critic        | Safety & constitution reviews                     |
| CryptoAnalyst | Live Binance + multi-TF RSI + funding + volume    |
| XGrowth       | High-signal X thread drafts (uses real Grok)      |
| SelfImprove   | Ranked proposals + **draft PRs with real files**  |
| Researcher    | Read-only summary of all open Issues              |

## How to use (30-second version)

1. Open or create an Issue  
2. Add a label (`crypto`, `x-growth`, `self-improve`, `research`, …)  
3. Comment `/run` or trigger the Action  
4. Read the agent comment (and any draft PR)

Full guide → [docs/USAGE.md](docs/USAGE.md)

## Autonomous features
- Daily briefing workflow (00:00 UTC)
- Agents can open draft PRs with real proposal files (never auto-merge)
- Real market data from public Binance endpoints
- Runner self-check on every run

## Safety
- Constitution + human-approved path for core changes
- Agents never force-merge
- File writes limited to safe paths (`proposals/`, `memory/`, `skills/`, `docs/`, `tests/`)
- Research / crypto outputs always carry disclaimers
