# RepoMind Agents

| Agent            | Labels                              | Role                                              |
|------------------|-------------------------------------|---------------------------------------------------|
| Critic           | `task`, `agent`, `critic`, `review` | Default safety / constitution reviews             |
| CryptoAnalyst    | `crypto`, `ta`, `scan`              | Live Binance multi-TF RSI + funding + volume      |
| XGrowth          | `x-growth`, `growth`, `thread`      | High-signal thread drafts (LLM-aware)             |
| SelfImprove      | `self-improve`, `evolve`            | Ranked proposals + draft PRs with real files      |
| Researcher       | `research`, `researcher`, `summary` | Read-only summary of open Issues                  |

## SelfImprove draft PR trigger words
Include any of: `pr`, `pull request`, `draft`, `implement`, `open pr`, `create pr`

## Safety
- All agent PRs are **draft only**
- File writes restricted to safe path prefixes
- Nothing merges without human approval
