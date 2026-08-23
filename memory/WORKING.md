# Working Memory

**Current phase:** 1b – Runtime wired, first skills live

## Active components
- core/: models, agent_base, github_client, llm, safety, orchestrator, skill_loader
- agents/base_runner.py (now called by the workflow)
- skills/crypto/ta_scanner + skills/x_growth/thread_factory

## Next focus
- Real specialized agents that load skills and call LLM
- Expand TA scanner with more indicators
- Better thread style examples for X growth
- Self-improve skill
- Tests
