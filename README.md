# RepoMind

**GitHub-native multi-agent OS**  
The repository *is* the runtime. Issues = tasks. Actions = compute. Agents evolve the system.

## Status: Phase 3a

Five specialized agents + autonomous daily briefing.

| Agent         | What it does                                      |
|---------------|---------------------------------------------------|
| Critic        | Safety & constitution reviews                     |
| CryptoAnalyst | Live Binance + multi-TF RSI + funding + volume    |
| XGrowth       | High-signal X thread drafts (uses real Grok)      |
| SelfImprove   | Ranked proposals + **real draft PRs** when asked  |
| Researcher    | Read-only summary of all open Issues              |

## How to use (30-second version)

1. Open or create an Issue  
2. Add a label (`crypto`, `x-growth`, `self-improve`, `research`, …)  
3. Comment `/run` or trigger the Action  
4. Read the agent comment (and any draft PR)

Full guide → [docs/USAGE.md](docs/USAGE.md)

## Autonomous features
- Daily briefing workflow (00:00 UTC) posts Researcher + Crypto summaries
- Agents can open draft PRs (never auto-merge)
- Real market data from public Binance endpoints

## Safety
- Constitution + human-approved path for core changes
- Agents never force-merge
- Research / crypto outputs always carry disclaimers
