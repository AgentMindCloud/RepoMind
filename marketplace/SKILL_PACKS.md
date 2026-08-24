# RepoMind Skill Packs (Phase 5)

Skill packs are versioned collections of skills that can be enabled together.

## Built-in packs

### core
- Always on
- Agents: Critic, Researcher, SelfImprove

### crypto-pro
- skills/crypto/ta_scanner
- Requires no private keys (public Binance endpoints)

### x-growth
- skills/x_growth/thread_factory
- Uses XAI_API_KEY when available

### self-evolve
- skills/self_improve/code_evolver
- Draft-PR only, safe paths only

## How to add a pack
1. Create a folder under `skills/<domain>/`
2. Add `SKILL.md` + `implementation.py`
3. Register the agent/skill in orchestrator if needed
4. Document it here

## Safety
- Packs never auto-merge code
- Marketplace is documentation + discovery for now (Phase 5 scaffolding)
