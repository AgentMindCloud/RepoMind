# Phase 8

## Goals
1. Green CI on every main commit (tests hard-fail, no phantom red workflows)
2. Real pack checksum verification helpers + tests
3. Keep all safety rails (draft PRs only, human-approved for core)
4. Optional later: pin computed sha256 into packs.json, tiny skill-diff guidance

## Status
Phase 8a live: CI hygiene + checksum tests.

## Safety unchanged
- Draft PRs only
- Safe-path writes only
- Never auto-merge
- No auto-post to X
