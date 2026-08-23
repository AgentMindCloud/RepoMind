# Working Memory

**Current phase:** 1d – Specialized agents live

## Active agents
- CriticAgent (safety + constitution)
- CryptoAnalystAgent (calls ta_scanner skill)
- XGrowthAgent (calls thread_factory skill)

## Skills
- crypto/ta_scanner (expanded mock indicators)
- x_growth/thread_factory (JanSol0s-style drafts)
- self_improve/code_evolver

## Runtime
- base_runner registers agents
- Orchestrator routes by labels
- Workflow calls the runner

## Next
- Better default agent / fallback
- LLM-backed skill bodies (after XAI_API_KEY)
- More tests + docs
- Live data adapters for TA
