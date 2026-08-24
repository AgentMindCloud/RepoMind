# RepoMind

**The multi-agent OS that lives inside a GitHub repository.**

Issues = tasks · Actions = compute · Agents = specialized roles · Skills = capabilities · PRs = evolution

Built phone-first. Runs entirely on GitHub. Powered by Grok.

---

## Status – Phase 2b

**Live agents**
| Agent | Trigger labels | What it does |
|-------|----------------|--------------|
| Critic | `task`, `agent` | Safe default review |
| Crypto Analyst | `crypto`, `ta` | Live prices + momentum bias (CoinGecko) |
| X-Growth | `x-growth`, `thread` | Draft high-signal X threads with Grok |
| Self-Improve | `self-improve` | Prioritized, actionable improvement proposals |

**Secret required:** `XAI_API_KEY` (already set and working)

---

## How to use (30 seconds)

1. Open or create an **Issue**
2. Add a label (`crypto` / `x-growth` / `self-improve` / `task`)
3. Comment `/run` or just wait
4. Read the agent reply on the Issue

Full guide → [docs/USAGE.md](docs/USAGE.md)

---

## Quick links

- [Issues](https://github.com/AgentMindCloud/RepoMind/issues)
- [Actions](https://github.com/AgentMindCloud/RepoMind/actions)
- [Changelog](CHANGELOG.md)

Built with Grok · AgentMindCloud
