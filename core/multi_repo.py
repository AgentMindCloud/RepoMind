"""Multi-repo helpers – Phase 6 (status + policy-aware)."""
from __future__ import annotations
from typing import Dict, Any, Optional, List
import os

try:
    import yaml
except ImportError:
    yaml = None

def load_repos_config(path: str = "config/repos.yaml") -> Dict[str, Any]:
    default = {
        "primary": {"owner": "AgentMindCloud", "name": "RepoMind", "default_branch": "main"},
        "satellites": [],
        "secondary": [],
        "rules": {
            "allow_cross_repo_comments": False,
            "allow_cross_repo_prs": False,
            "require_human_approval_for_satellites": True,
            "write_to_secondary": False,
            "draft_pr_only": True,
        },
        "policy": {
            "write_to_secondary": False,
            "draft_pr_only": True,
            "require_human_approved": True,
        },
    }
    if yaml is None:
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            # merge shallow defaults
            for k, v in default.items():
                data.setdefault(k, v)
            return data
    except Exception:
        return default

def primary_repo_full_name(cfg: Optional[Dict[str, Any]] = None) -> str:
    cfg = cfg or load_repos_config()
    primary = cfg.get("primary") or {}
    if isinstance(primary, str):
        return os.getenv("GITHUB_REPOSITORY", primary)
    owner = primary.get("owner") or "AgentMindCloud"
    name = primary.get("name") or "RepoMind"
    return os.getenv("GITHUB_REPOSITORY", f"{owner}/{name}")

def list_satellites(cfg: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    cfg = cfg or load_repos_config()
    sats = cfg.get("satellites") or cfg.get("secondary") or []
    out = []
    for s in sats:
        if isinstance(s, str):
            out.append({"name": s, "enabled": False})
        elif isinstance(s, dict):
            out.append(s)
    return out

def satellites_enabled(cfg: Optional[Dict[str, Any]] = None) -> bool:
    cfg = cfg or load_repos_config()
    rules = cfg.get("rules") or {}
    policy = cfg.get("policy") or {}
    sats = list_satellites(cfg)
    if not sats:
        return False
    if rules.get("require_human_approval_for_satellites", True):
        return False
    if policy.get("require_human_approved", True):
        return False
    return any(s.get("enabled") for s in sats)

def multi_repo_status(cfg: Optional[Dict[str, Any]] = None) -> str:
    """Human-readable multi-repo status for agent comments."""
    cfg = cfg or load_repos_config()
    primary = primary_repo_full_name(cfg)
    sats = list_satellites(cfg)
    rules = cfg.get("rules") or {}
    policy = cfg.get("policy") or {}
    lines = [
        f"**Primary:** `{primary}`",
        f"**Satellites configured:** {len(sats)}",
    ]
    for s in sats[:8]:
        name = s.get("name") or s.get("repo") or str(s)
        enabled = s.get("enabled", False)
        notes = s.get("notes", "")
        lines.append(f"- `{name}` · enabled={enabled}" + (f" · {notes}" if notes else ""))
    lines.append(
        f"**Policy:** write_secondary={policy.get('write_to_secondary', rules.get('write_to_secondary', False))} · "
        f"draft_only={policy.get('draft_pr_only', rules.get('draft_pr_only', True))} · "
        f"human_approval={policy.get('require_human_approved', rules.get('require_human_approval_for_satellites', True))}"
    )
    if not satellites_enabled(cfg):
        lines.append("_Cross-repo writes disabled until human enables satellites and relaxes approval policy._")
    return "\n".join(lines)
