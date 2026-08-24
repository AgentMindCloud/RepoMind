# Signed Skill Packs (Phase 7)

## Goal
Integrity pins for skill packs so humans can verify what they are about to enable.

## Current scheme
- Manifest: `marketplace/packs.json`
- Field: `checksum_sha256` (advisory)
- Status values may be `pending-local-compute` until a maintainer fills real hashes

## How to pin a pack
1. Hash the pack entry file (usually `implementation.py`)
2. Put the sha256 into `packs.json`
3. Keep `pinned: true`
4. Open a draft PR — never auto-merge

## Rules
- Agents never claim a pack is cryptographically signed unless a real signature scheme is implemented
- Human review still required
- Prefer pinned packs for default routing
