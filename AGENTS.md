# RepoMind Agents

| Agent            | Labels                              | Role                                              |
|------------------|-------------------------------------|---------------------------------------------------|
| Critic           | `task`, `agent`, `critic`, `review` | Default safety / constitution reviews             |
| CryptoAnalyst    | `crypto`, `ta`, `scan`              | Live Binance multi-TF RSI + funding + volume + OI |
| XGrowth          | `x-growth`, `growth`, `thread`      | High-signal thread drafts (LLM-aware)             |
| SelfImprove      | `self-improve`, `evolve`            | Ranked proposals + draft PRs + skill micro-notes  |
| Researcher       | `research`, `researcher`, `summary` | Read-only summary of open Issues                  |

## SelfImprove draft PR trigger words
Include any of: `pr`, `pull request`, `draft`, `implement`, `open pr`, `create pr`

## SelfImprove safe writes
- `proposals/`
- `memory/`
- `skills/*/IMPROVE_NOTES.md` (gated micro-notes only)

## Safety
- All agent PRs are **draft only**
- Nothing merges without human approval
