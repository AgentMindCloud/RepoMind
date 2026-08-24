# Human-Approved Merge Gate (Phase 7)

Agents may open **draft PRs only**. Nothing merges automatically.

## Required checklist before merge

- [ ] Review every file path in the PR
- [ ] Confirm only allow-listed prefixes changed (`proposals/`, `docs/`, `skills/`, `memory/`, `tests/`, `marketplace/`)
- [ ] No secrets, tokens, or credentials present
- [ ] Market skills still include NFA disclaimer if touched
- [ ] Add label `human-approved` on the Issue or PR description when ready
- [ ] Merge only after the above is true

## Agent rules
- Never remove the draft status themselves
- Never force-push main
- Never claim approval on behalf of a human
