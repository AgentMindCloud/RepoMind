# Phone Workflow – RepoMind

Everything runs from GitHub mobile + Actions. No local machine required for normal use.

## Daily loop
1. Open or create an Issue on GitHub mobile.
2. Add one of these labels:
   - `task` or `agent` → Critic (safe default)
   - `crypto` / `ta` → CryptoAnalystAgent
   - `x-growth` / `thread` → XGrowthAgent
3. The scheduled / event-driven workflow runs `agents/base_runner.py`.
4. Agents comment results or drafts directly on the Issue.
5. Review on your phone. Merge any PRs that appear.
6. For changes to `core/` or `contracts/`: add the `human-approved` label before merge.

## Secrets (do once on PC)
- `XAI_API_KEY` (required for real LLM power)
- Optional: X API keys later for live posting skills

## Manual trigger
Actions → RepoMind Agent Runner → Run workflow → optionally pass an issue number.
