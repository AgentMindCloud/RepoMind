# Skill Pack Install Flow (Phase 6)

RepoMind does **not** auto-install remote code.

## Safe install path

1. Human opens an Issue titled e.g. `Install skill pack: crypto-pro`
2. Label: `self-improve` or `task`
3. Body includes: `install pack <id>` and preferably `create pr`
4. SelfImprove / Critic may open a **draft PR** that:
   - updates `marketplace/registry.yaml` status notes
   - adds a local skill stub under `skills/` only if the pack is already trusted/local
5. Human reviews and merges

## Forbidden
- Downloading arbitrary remote code without human review
- Writing outside safe paths
- Auto-merging install PRs

## Trusted local packs
See `marketplace/registry.yaml` for live pack IDs.
