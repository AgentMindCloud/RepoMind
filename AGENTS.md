# RepoMind Agents

| Agent            | Labels                              | Role                                              |
|------------------|-------------------------------------|---------------------------------------------------|
| Critic           | `task`, `agent`, `critic`, `review` | Default safety / constitution reviews             |
| CryptoAnalyst    | `crypto`, `ta`, `scan`              | Live Binance multi-TF RSI + funding scans         |
| XGrowth          | `x-growth`, `growth`, `thread`      | High-signal thread drafts (LLM-aware)             |
| SelfImprove      | `self-improve`, `evolve`            | Ranked proposals + real draft PRs when asked      |
| Researcher       | `research`, `researcher`, `summary` | Read-only summary of open Issues                  |

All agents comment on the Issue. Nothing is auto-merged.
