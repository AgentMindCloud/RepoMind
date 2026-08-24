# Long-Term Memory

## Architecture Decisions
- The GitHub repository *is* the OS.
- Issues = task board / Kanban
- PRs = self-evolution mechanism
- Actions = compute engine
- Constitution in contracts/constitution.yaml is the safety source of truth
- Skills use SKILL.md (open standard) + Python implementation
- Primary model: xAI Grok via XAI_API_KEY secret
- Draft PRs only; never auto-merge
- Agents never auto-post to X

## Lessons
- Phone-first development works when everything is pure text + GitHub primitives
- Keep modules small so mobile review stays easy
- Human-in-the-loop for core changes and live X posts is non-negotiable
- Safe-path allow-lists for agent file writes prevent accidental core damage
- Live public market data (Binance) is enough for useful research heuristics without API keys

## Phase milestones
- Phase 1: Core multi-agent runtime + phone workflow
- Phase 2: Live data, multi-TF RSI, funding, Researcher, draft PRs
- Phase 3: Volume, daily briefing, real proposal files in draft PRs
- Phase 4: Open Interest, weekly X-Growth drafts, richer self-evolution path

## Durable patterns that work
- Label-based routing is simple and reliable from mobile
- Structured agent comments with "Next actions for you" reduce friction
- Draft PRs with real content under proposals/ make self-evolution tangible
