"""Multi-repo readiness helpers – Phase 5 scaffolding."""
from __future__ import annotations
from typing import Dict, Any, Optional
import os

try:
    import yaml
except ImportError:
    yaml = None

def load_repos_config(path: str = "config/repos.yaml") -> Dict[str, Any]:
    if yaml is None:
        return {
            "primary": {
                "owner": "AgentMindCloud",
                "name": "RepoMind",
                "default_branch": "main",
            },
            "satellites": [],
            "rules": {
                "allow_cross_repo_comments": False,
                "allow_cross_repo_prs": False,
                "require_human_approval_for_satellites": True,
            },
        }
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}

def primary_repo_full_name(cfg: Optional[Dict[str, Any]] = None) -> str:
    cfg = cfg or load_repos_config()
    primary = cfg.get("primary") or {}
    owner = primary.get("owner") or "AgentMindCloud"
    name = primary.get("name") or "RepoMind"
    return os.getenv("GITHUB_REPOSITORY", f"{owner}/{name}")

def satellites_enabled(cfg: Optional[Dict[str, Any]] = None) -> bool:
    cfg = cfg or load_repos_config()
    rules = cfg.get("rules") or {}
    sats = cfg.get("satellites") or []
    return bool(sats) and not rules.get("require_human_approval_for_satellites", True)
