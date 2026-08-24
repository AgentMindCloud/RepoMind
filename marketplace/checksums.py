"""Advisory checksum helpers for skill packs – Phase 8."""
from __future__ import annotations
import hashlib
import json
import os
from typing import Dict, Any, Optional, List

def sha256_file(path: str) -> Optional[str]:
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_packs(path: str = "marketplace/packs.json") -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"packs": [], "policy": {}}

def compute_pack_checksums(packs_path: str = "marketplace/packs.json") -> List[Dict[str, Any]]:
    """Return actual sha256 for each pack entry file."""
    data = load_packs(packs_path)
    out = []
    for p in data.get("packs") or []:
        entry = p.get("entry") or "implementation.py"
        rel = os.path.join(p.get("path", ""), entry)
        actual = sha256_file(rel)
        out.append({
            "id": p.get("id"),
            "path": rel,
            "actual": actual,
            "expected": p.get("checksum_sha256"),
            "matches": bool(
                actual
                and p.get("checksum_sha256")
                and p.get("checksum_sha256") != "pending-local-compute"
                and actual == p.get("checksum_sha256")
            ),
        })
    return out

def verify_pack(pack_id: str, packs_path: str = "marketplace/packs.json") -> Dict[str, Any]:
    data = load_packs(packs_path)
    packs = data.get("packs") or []
    target = next((p for p in packs if p.get("id") == pack_id), None)
    if not target:
        return {"ok": False, "error": f"unknown pack: {pack_id}"}
    entry = target.get("entry") or "implementation.py"
    rel = os.path.join(target.get("path", ""), entry)
    actual = sha256_file(rel)
    expected = target.get("checksum_sha256")
    pinned_ok = bool(actual and expected and expected != "pending-local-compute" and actual == expected)
    return {
        "ok": bool(actual),  # file exists
        "pinned_match": pinned_ok,
        "pack_id": pack_id,
        "path": rel,
        "actual": actual,
        "expected": expected,
        "pinned": bool(target.get("pinned")),
        "advisory_only": True,
    }

def verify_all_pack_paths(packs_path: str = "marketplace/packs.json") -> bool:
    """True if every pack entry file exists on disk."""
    rows = compute_pack_checksums(packs_path)
    return all(r.get("actual") for r in rows)
