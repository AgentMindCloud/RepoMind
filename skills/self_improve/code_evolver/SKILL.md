# Skill: Code Evolver (Self-Improve)

**Name:** code_evolver  
**Version:** 0.1.0  
**Category:** self_improve  
**Safety:** high

## Description
Analyzes recent Actions logs, Issue outcomes, and code quality signals, then proposes small improvements via draft PRs or Issue comments.

## Inputs
- focus: str (optional – "skills", "core", "tests", "docs")

## Outputs
- proposals: list[str]
- summary: str

## Notes
- Never force-merges
- Always respects Constitution
- Prefers tiny, reviewable changes
