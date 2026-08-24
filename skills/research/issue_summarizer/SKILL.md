# Skill: Issue Summarizer (Researcher)

**Version:** 0.1.0  
**Safety:** high – read-only

## Description
Summarizes open GitHub Issues grouped by primary label. Used by the Researcher agent.

## Inputs
- `issues`: list of issue dicts (`number`, `title`, `labels`)

## Outputs
- Markdown summary
- Counts by label
- Suggested next actions

## Rules
- Read-only
- Never modifies code or opens PRs
