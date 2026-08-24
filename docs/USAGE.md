# How to Use RepoMind (Simple Guide)

RepoMind is a multi-agent system that lives inside this GitHub repository.
You control it by opening Issues and adding labels. Agents then do the work and comment back.

---

## The Only Thing You Need to Remember

**Issue + Label = Agent runs**

That's it.

---

## Step-by-step (works from phone or PC)

### 1. Create or open an Issue
Go to: https://github.com/AgentMindCloud/RepoMind/issues

Write a short title, for example:
- "Scan BTC ETH SOL"
- "Draft a thread about building agents from phone"
- "Review this idea for safety"

### 2. Add the right label

| What you want | Label to add |
|---------------|--------------|
| Safe default / review | `task` or `agent` or `critic` |
| Crypto TA scan | `crypto` or `ta` |
| X / Twitter thread draft | `x-growth` or `growth` or `thread` |
| Suggest improvements to the repo | `self-improve` or `evolve` |

### 3. Wait a moment
GitHub Actions will start the agent (usually under 1 minute).
You can also force it:
- Comment `/run` on the Issue, **or**
- Go to Actions → "RepoMind Agent Runner" → Run workflow → type the Issue number

### 4. Read the result
The agent posts a comment directly on the Issue with the result, draft, or proposal.

### 5. Review
- Like the draft? Copy it and post (or improve it).
- Want changes? Reply on the Issue or open a new one.
- Safety-sensitive changes need a `human-approved` label before merge.

---

## Examples

**Crypto scan**
1. New Issue titled "3H TA scan"
2. Add label `crypto`
3. Agent comments a multi-asset scan with disclaimer

**Thread draft**
1. New Issue titled "Thread about phone-first Grok agents"
2. Add label `x-growth`
3. Agent comments a ready-to-edit thread draft

**Improve the system itself**
1. New Issue titled "Make TA skill use live data"
2. Add label `self-improve`
3. Agent proposes concrete next steps

---

## Secrets (already done)
You already added `XAI_API_KEY`. That is the only required secret for real Grok power.

---

## Tips
- You can run multiple Issues at the same time.
- Agents never auto-post to X. They only draft.
- Everything stays inside GitHub so you can work fully from your phone.
