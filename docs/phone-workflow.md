# Phone Workflow – RepoMind

Everything runs from GitHub mobile + Actions. No local machine required for normal use.

## Daily loop
1. Open or create an Issue on GitHub mobile.
2. Add one of these labels:
   - `task` / `agent` / `critic` → Critic (safe default)
   - `crypto` / `ta` → CryptoAnalystAgent
   - `x-growth` / `growth` / `thread` → XGrowthAgent
   - `self-improve` / `evolve` → SelfImproveAgent
3. The workflow runs `agents/base_runner.py`.
4. Agents comment results or drafts directly on the Issue.
5. Review on your phone.

## Manual trigger (when you want it now)
- Comment `/run` on the Issue, **or**
- Actions → RepoMind Agent Runner → Run workflow → type the Issue number

## Secrets (already done)
- `XAI_API_KEY` is set → real Grok power is available

## Full simple guide
See [USAGE.md](USAGE.md) for the clearest step-by-step instructions.
