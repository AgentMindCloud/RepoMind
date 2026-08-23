# Changelog

## [Unreleased] / Phase 1h – 1i

### Added
- Four specialized agents: Critic (default), CryptoAnalyst, XGrowth, SelfImprove
- CI test workflow (`.github/workflows/tests.yml`)
- Phone workflow docs
- Basic orchestrator routing tests
- Self-improve skill with concrete proposal list
- Expanded X-Growth thread_factory (magnetic templates + visual ideas)

### Changed
- Orchestrator now auto-registers all four agents
- TA scanner interface cleaned (accepts symbols / timeframe flexibly)
- README and memory kept in sync with current phase

### Notes
- Full LLM power still requires `XAI_API_KEY` secret (to be added on PC)
- Real market data for CryptoTA is the next major unlock
