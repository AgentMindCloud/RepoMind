# Phase 6 Complete

## Goals achieved
1. Multi-repo status orchestration (read-only by default)
2. Skill pack install flow with human approval scaffolding
3. SelfImprove minimal gated code sketches in draft PRs
4. Safety rails retained: draft-only, safe paths, human-approved merges

## How to use new Phase 6 features

### Multi-repo status
Label an Issue `research` and `/run` — Researcher includes multi-repo status.

### Install pack request
Create Issue with body containing `install pack <id>` and `create pr`, label `self-improve`, then `/run`.

### Minimal code sketches
SelfImprove draft PRs may include files under `proposals/patches/` with illustrative minimal diffs. Humans integrate before merge.
